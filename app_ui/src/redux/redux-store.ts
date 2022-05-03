import { configureStore } from '@reduxjs/toolkit'
import authReduser from './authReduser';


export const store = configureStore({
  reducer: {
    auth: authReduser,
  }
})

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<typeof store.getState>
// Inferred type: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch
// @ts-ignore
window.__store__ = store
export default store