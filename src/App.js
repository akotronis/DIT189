import { Route, Routes } from 'react-router-dom';
import RootLayout from './layouts/RootLayout';
import Dashboard from './pages/Dashboard';
import LoginScreen from './pages/LoginScreen';
import { ProtectedRoute } from './routes/ProtectedRoute';
import { ChakraProvider, theme } from '@chakra-ui/react';
import { AuthProvider } from './context/Auth';
// import theme from './theme';
// const router = createBrowserRouter(
//   createRoutesFromElements(
//     <Route path="/" element={<RootLayout />}>
//       <Route
//         index
//         element={
//             <LoginScreen>
//               <Dashboard />
//              </LoginScreen>
//         }
//       />
//       {/* <Route path="/profile" element={<Profile />} /> */}
//       {/* <Route path="/create" element={<Create />} action={createAction} /> */}
//     </Route>
//   )
// );

function App() {
  return (
    <ChakraProvider theme={theme}>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<LoginScreen />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
              <RootLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
          </Route>
        </Routes>
      </AuthProvider>
    </ChakraProvider>
  );
}

export default App;
