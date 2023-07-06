import {
  Box,
  Button,
  Flex,
  HStack,
  Heading,
  Spacer,
  Text,
} from '@chakra-ui/react';

export default function Navbar() {
  return (
    <Flex as="nav" p="10px" alignItems="center" marginBottom="40px">
      <Heading as="h1">e-Divorce</Heading>
      <Spacer />
      <HStack spacing="20px">
        <Box bg="gray.200" p="10px">
          M
        </Box>
        <Text>rocketleague@gmail.com</Text>
        <Button colorScheme="blue">Logout</Button>
      </HStack>
    </Flex>
  );
}
