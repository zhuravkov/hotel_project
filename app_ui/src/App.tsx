import React, { useState } from 'react'

import { useAppDispatch, useAppSelector } from './hooks/appHooks'
import { authUserThunk } from './redux/authReduser'


const App = () => {
  // The `state` arg is correctly typed as `RootState` already
  const user = useAppSelector(state => state.auth)
  const dispatch = useAppDispatch()
  return (
    <div>
        <div>{user.userId || "userId"}</div>
        <div>{user.email || "email"}</div>
        <div>{user.isAuth ? "isAuth" : "Not Auth"}</div>

        <button  onClick={() => dispatch(authUserThunk())} >redux</button>


    </div>
  )
  // omit rendering logic
}

export default App
