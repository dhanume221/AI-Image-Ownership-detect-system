import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/', // Adjust if backend port differs
    timeout: 10000,
});

export default api;
