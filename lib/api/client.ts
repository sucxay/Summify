const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

if (!API_BASE_URL) {
  throw new Error('NEXT_PUBLIC_API_URL is not configured.');
}

export class ApiError extends Error {
  status: number;
  detail: unknown;
  code?: string;

  constructor(message: string, status: number, detail?: unknown, code?: string) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
    this.code = code;
  }
}

type RequestOptions = RequestInit & {
  timeoutMs?: number;
};

type JsonRecord = Record<string, unknown>;

async function parseResponse(response: Response): Promise<unknown> {
  const contentType = response.headers.get('content-type') ?? '';
  if (contentType.includes('application/json')) {
    return response.json();
  }

  const text = await response.text();
  return text ? { detail: text } : null;
}

function getErrorMessage(payload: unknown, fallback: string): string {
  if (payload && typeof payload === 'object') {
    const record = payload as JsonRecord;
    if (typeof record.message === 'string') {
      return record.message;
    }
    if (typeof record.detail === 'string') {
      return record.detail;
    }
    if (Array.isArray(record.detail)) {
      return 'Request validation failed.';
    }
  }

  return fallback;
}

export async function requestJson<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const controller = new AbortController();
  const timeoutMs = options.timeoutMs ?? 60000;
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      signal: controller.signal,
      headers: {
        Accept: 'application/json',
        ...(options.headers ?? {}),
      },
    });

    const payload = await parseResponse(response);
    if (!response.ok) {
      const detail = payload && typeof payload === 'object' ? payload : null;
      const code = detail && typeof detail === 'object' && typeof (detail as JsonRecord).error === 'string'
        ? ((detail as JsonRecord).error as string)
        : undefined;
      throw new ApiError(getErrorMessage(payload, 'Request failed.'), response.status, payload, code);
    }

    return payload as T;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }

    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new ApiError('The request timed out. Please try again.', 408);
    }

    throw new ApiError('Unable to reach the backend. Confirm the FastAPI server is running.', 0);
  } finally {
    window.clearTimeout(timeoutId);
  }
}

export function uploadMultipart<T>(
  path: string,
  formData: FormData,
  onProgress?: (progress: number) => void,
): Promise<T> {
  return new Promise((resolve, reject) => {
    const request = new XMLHttpRequest();
    request.open('POST', `${API_BASE_URL}${path}`);
    request.responseType = 'json';
    request.timeout = 120000;
    request.setRequestHeader('Accept', 'application/json');

    request.upload.onprogress = (event) => {
      if (event.lengthComputable && onProgress) {
        onProgress(Math.round((event.loaded / event.total) * 100));
      }
    };

    request.onerror = () => {
      reject(new ApiError('Unable to reach the backend. Confirm the FastAPI server is running.', 0));
    };

    request.ontimeout = () => {
      reject(new ApiError('The upload timed out. Please try again.', 408));
    };

    request.onload = () => {
      const payload = request.response ?? null;
      if (request.status >= 200 && request.status < 300) {
        resolve(payload as T);
        return;
      }

      const fallback = request.status === 0 ? 'Upload failed.' : 'The backend rejected the upload.';
      const code = payload && typeof payload === 'object' && typeof (payload as JsonRecord).error === 'string'
        ? ((payload as JsonRecord).error as string)
        : undefined;
      reject(new ApiError(getErrorMessage(payload, fallback), request.status, payload, code));
    };

    request.send(formData);
  });
}

export { API_BASE_URL };
