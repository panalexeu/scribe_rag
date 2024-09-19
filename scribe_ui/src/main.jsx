import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import {
    createBrowserRouter,
    RouterProvider
} from "react-router-dom";

const router = createBrowserRouter([
  {
    path: '/',
    element: <div>Hello, World!</div>
  }
])

createRoot(document.getElementById('root')).render(
    <StrictMode>
      <RouterProvider router={router}></RouterProvider>
    </StrictMode>,
)
