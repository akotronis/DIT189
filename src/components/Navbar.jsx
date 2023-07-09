import {
  Button,
  Flex,
  HStack,
  Heading,
  Spacer,
  Text,
} from '@chakra-ui/react';

import { useCallback } from 'react';
import { useAuth } from "../context/Auth";
import { useNavigate } from 'react-router-dom';

export default function Navbar() {

  const { user, setUser } = useAuth();
  const navigate = useNavigate();

  const logout = useCallback(
    (e) => {
      e.preventDefault();
      setUser(null);
      navigate("/");
    },
    [navigate, setUser]
  );

  return (
    <Flex as="nav" p="10px" alignItems="center" marginBottom="40px" backgroundColor={'blue.500'}>
      <Heading as="h1" color={"white"}>e-Divorce</Heading>
      <Spacer />
      <HStack spacing="20px">
        <Text color={"white"}>rocketleague@gmail.com</Text>
        <Button colorScheme="blue" onClick={logout}>Logout</Button>
      </HStack>
    </Flex>
  );
}
