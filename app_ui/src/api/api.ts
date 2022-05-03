import axios from 'axios';

// создаем инстанс аксиоса чтобы сохранить в 1 месте все настройки и потом обращаться к ним
const instance = axios.create({
    baseURL: 'http://localhost:8000/api/',
    withCredentials: true
});


// работаем с Success а по факту там число
export enum ResultCodesEnum {
    Success = 0,
    Error = 1
}


type AuthMeResponseTypes = {
    data : {
        userId : number
        email : string
    }
    resultCode : ResultCodesEnum
    messages : string
}

export const authAPI = {
    async authMe () {
        const response = await instance.get<AuthMeResponseTypes>(`auth/me`);
        return response.data;
    },
    login (email:string, password:string) {
        return instance.post(`/login`, {email, password})
        .then(response => response.data);
    },
    logout () {
        return instance.delete(`/login`)
        .then(response => response.data);
    },
}
// authAPI.authMe().then(res=>res.t)
instance.get<string>(`auth/me`).then((res)=>res.data.toUpperCase)
// // для удобства работы упаковываем методы апишек(можно по эндпоинтам) в объекты

// export const usersAPI = {
//     getUsers (currentPage, pageSize) {
//     return instance.get(`users?page=${currentPage}&on_page=${pageSize}`) 
//         // возващаем в промисе не всё что пришло в response а только data
//         .then(response => response.data);
// }};

// export const folowingAPI = {
//     unfollowAPI (id) {
//         return instance.delete(`follow/${id}`)
//         .then(response => response.data);
//     },
//     followAPI (id) {
//         return instance.post(`follow/${id}`,{})
//         .then(response => response.data);
//     },
//     checkFollowingAPI (id) {
//         return instance.get(`follow/${id}`)
//         .then(response => response.data);
//     },
// }



// export const profileAPI = {
//     usersProfile (id) {
//         return instance.get(`profile/${ id }`)
//         .then(response => response.data);
//     },
//     getStatus (id) {
//         return instance.get(`profile/status/${ id }`)
//         .then(response => response.data);
//     },
//     updateStatus(status) {
//         return instance.put(`profile/status`, { status : status })
//         .then(response => response.data);
//     }




// }