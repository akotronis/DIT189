import React from 'react';
import { Flex, Box } from '@chakra-ui/react';
import { Outlet } from 'react-router-dom';
import Navbar from '../components/Navbar';

const customStyles = {
  height: '100vh',
  backgroundColor: '#ebebeb', // Change the background color as desired
};

export default function RootLayout() {
  return (
    <Flex direction="column" align="center" style={customStyles}>
      <Box w="100%">
        <Navbar />
      </Box>
        <Box
          w="95%"
          p="20px"
          borderRadius="10px"
          bg="white"
          boxShadow="0px 2px 4px rgba(0, 0, 0, 0.2)"
        >
          <Outlet />
        </Box>
    </Flex>
  );
}
// <Grid templateColumns="repeat(6, 1fr)" bg="gray.50">
//   <GridItem
//     as="aside"
//     colSpan={{ base: 6, lg: 2, xl: 1 }}
//     bg="blue.400"
//     minHeight={{lg: "100vh"}}
//     p={{ base: '20px', lg: '30px' }}
//   >
//     <span><Sidebar/></span>
//   </GridItem>
//   <GridItem as="main" colSpan={{ base: 6, lg: 4, xl: 5 }} p="40px">
//     <Navbar />
//     <Outlet />
//   </GridItem>
// </Grid>
//   );
// }
