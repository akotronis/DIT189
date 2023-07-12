import {
  HStack,
  Text,
  Box,
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Flex,
  Heading,
  Button,
  Divider,
  CircularProgress,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react';
import { EditIcon } from '@chakra-ui/icons';
import { useDisclosure } from '@chakra-ui/react';
export default function CardCase(props) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Modal Title</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <Text>{props.case.description}</Text>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={onClose}>
              Close
            </Button>
            <Button variant="ghost">Secondary Action</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <Card
        key={props.case.id}
        borderTop="8px"
        borderColor="blue.400"
        bg="white"
      >
        <CardHeader>
          <Heading size="md">Case #15</Heading>
        </CardHeader>
        <CardHeader>
          <Flex gap={5}>
            <Box w="50px" h="50px" bg="red.100">
              <Text></Text>
            </Box>
            <Box>
              <Heading as="h3" size="sm">
                {props.case.id}
              </Heading>
              <Text>by {props.case.name}</Text>
            </Box>
          </Flex>
        </CardHeader>
        <CardBody>
          <Text color="gray.500">{props.case.description}</Text>
        </CardBody>
        <Divider borderColor="gray.200" />
        <CardFooter>
          <Flex
            width="100%"
            alignItems="center"
            gap={5}
            justifyContent={'space-between'}
          >
            <Button
              onClick={onOpen}
              variant="solid"
              bg="red.400"
              color="white"
              leftIcon={<EditIcon />}
            >
              Review
            </Button>
            <HStack>
              <Text>Waiting for second lawyer</Text>
              <CircularProgress
                value={30}
                color="orange.400"
                thickness="12px"
              />
            </HStack>
          </Flex>
        </CardFooter>
      </Card>
    </>
  );
}
