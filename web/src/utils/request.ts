import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse } from 'axios';

// Define API response types
interface GenerateRequest {
  owner: string;
  repo: string;
  wiki_path: string;
  wiki_url: string;
  files?: string[];
}

interface BaseResponse {
  success: boolean;
  message: string;
  data: any;
}

// Create axios instance
const instance: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '', // Use Vite environment variables
  timeout: 10000, // Request timeout
});

// Request interceptor
instance.interceptors.request.use(
  (config) => {
    // Here you can add token or other request headers
    // For example: config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
instance.interceptors.response.use(
  (response) => {
    // Here you can process response data
    return response;
  },
  (error) => {
    // Handle error response
    return Promise.reject(error);
  }
);

// Generic request function
export const request = async <T = any>(config: AxiosRequestConfig): Promise<T> => {
  const response = await instance(config);
  return response.data;
};

// API call functions
export const generateDoc = async (data: GenerateRequest): Promise<BaseResponse> => {
  return request<BaseResponse>({ method: 'POST', url: '/agents/generate', data });
};

export const listDocs = async (): Promise<BaseResponse> => {
  return request<BaseResponse>({ method: 'GET', url: '/agents/list' });
};

export const getWikiContent = async (repoId: string): Promise<string> => {
  return request<string>({ method: 'GET', url: `/wikis/${repoId}/index.html` });
};