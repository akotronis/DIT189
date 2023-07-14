import React from 'react';
import UserInfo from '../components/UserInfo';
import Navbar from '../components/Navbar';
import Dashboard from '../pages/Dashboard';
import { GridItem, Grid } from '@chakra-ui/react';
import { LoggedInHOC } from './LoggedinHOC';
export default function RootLayout() {
  return (
    <Grid templateColumns="repeat(6, 1fr)" h="100%" gap={4}>
      <GridItem
        as="header"
        colSpan={6}
        bg="blue.400"
        minHeight="60px"
        bgGradient="linear(to-r, blue.400, teal.400)"
        boxShadow="0px 5px 10px rgba(0, 0, 0, 0.4)"

      >
        <Navbar />
      </GridItem>
      <GridItem
        as="aside"
        colSpan={{ base: 6, lg: 2, xl: 1 }}
        p="20px"
        boxShadow="5px 5px 12px rgba(0, 0, 0, 0.5)"
        m="15px"
        borderRadius={"8px"}
      >
        <LoggedInHOC>
          <UserInfo />
        </LoggedInHOC>
      </GridItem>
      <GridItem as="main" colSpan={{ base: 6, lg: 4, xl: 5 }} p="40px" >
        <LoggedInHOC>
          <Dashboard />
        </LoggedInHOC>
      </GridItem>
    </Grid>
  );
}
