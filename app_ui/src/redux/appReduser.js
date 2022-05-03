
import { authAPI } from './../api/api';
import { authUserThunk } from './authReduser';

const SET_INITIALIZED= 'SET_INITIALIZED';




let inicialState = {
    initialized : false,
}

const appReduser = (state = inicialState, action) => {
    
    switch (action.type) {
        case SET_INITIALIZED:
            return {
                ...state,
                initialized : true
                }

        default:
            return state;
    }


}


const initializedSuccess = () => ({type: SET_INITIALIZED})




export const initializeThunk = () => (dispatch) =>{
    // dispath возвращает промис, для этого указали return в authUserThunk
    // ждём оттуда ответ и продолжаем
    let promise = dispatch(authUserThunk());
    // dispatch(something#2())
    // dispatch(something#3())
    // для несольких промисов Promise.all([promise, promis2...]) :
    Promise.all([promise])
        .then( ()=> {
            dispatch(initializedSuccess());
    });
}

    
    



export default appReduser