import { AnyAction, createAsyncThunk, createSlice, PayloadAction, ThunkAction } from '@reduxjs/toolkit'
import { authAPI, ResultCodesEnum } from '../api/api'
import store, { RootState } from './redux-store'


// Define a type for the slice state
type AuthState = {
    userId : number | null,
    email : string | null,
    isAuth : boolean
}

// Define the initial state using that type
const initialState:AuthState = {
    userId : null,
    email : null,
    isAuth : false
}




export const authSlice = createSlice({
  name: 'auth',
  // `createSlice` will infer the state type from the `initialState` argument
  initialState,
  reducers: {
    authMe : (state, action: PayloadAction<AuthState>) => {
        state.userId = action.payload.userId
        state.email = action.payload.email
        state.isAuth = action.payload.isAuth
    }
  }
})

export const { authMe } = authSlice.actions

// Other code such as selectors can use the imported `RootState` type
export const selectCount = (state: RootState) => {
    return {
        userId:state.auth.userId,
        email: state.auth.email,
        isAuth: state.auth.isAuth
    }
}


export type AuthThunkType = {
userId :number,
email : string,
isAuth : boolean
}

export const authUserThunk = (): ThunkAction<Promise<void>, RootState, unknown, AnyAction> => 
async (dispatch,getState) => {
    // let a = getState().auth.isAuth
    let data = await authAPI.authMe();
    if (data.resultCode === ResultCodesEnum.Success ) {
        let payload = {...data.data, isAuth:true}
        dispatch(authMe(payload))
    }
 }


export default authSlice.reducer
