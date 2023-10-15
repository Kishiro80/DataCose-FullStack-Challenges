// api.js
const create = async (axios, root, data, route = 'create/') => {
    try {
        const response = await axios.post(`/${root}/${route}`, data);
        return response.data;
    } catch (error) {
        console.error(`Error creating ${root}:`, error);
        throw error;
    }
};

const get = async (axios, root, id, route = 'id/') => {
    try {
        const response = await axios.get(`/${root}/${route}`, { params: { id } });
        return response.data;
    } catch (error) {
        console.error(`Error getting ${root}:`, error);
        throw error;
    }
};

const getAll = async (axios, root, params, route = 'all/') => {
    try {
        const response = await axios.get(`/${root}/${route}`, { params: params });
        return response.data;
    } catch (error) {
        console.error(`Error getting all ${root}:`, error);
        throw error;
    }
};

const search = async (axios, root, params, route = 'search/') => {
    try {
        const response = await axios.get(`/${root}/${route}`, { params: params });
        return response.data;
    } catch (error) {
        console.error(`Error searching ${root}:`, error);
        throw error;
    }
};

const update = async (axios, root, id, data) => {
    try {
        const response = await axios.put(`/${root}/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error(`Error updating ${root}:`, error);
        throw error;
    }
};

const deleteOne = async (axios, root, id) => {
    try {
        const response = await axios.delete(`/${root}/`, { params: { id } });
        return response.data;
    } catch (error) {
        console.error(`Error deleting ${root}:`, error);
        throw error;
    }
};

export { create, get, getAll, search, update, deleteOne };
