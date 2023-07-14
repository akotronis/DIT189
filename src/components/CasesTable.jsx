import {
  Button,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  TableContainer,
  Table,
  Thead,
  Tr,
  Th,
  Td,
  Tbody,
  Tag,
  TagLabel,
  Box,
  HStack,
  Flex,
} from '@chakra-ui/react';
import { useState } from 'react';
import CaseView from './CaseView';
import { getCaseMessage, getUsers } from '../utils/api_utils';
import { useAccessToken } from '../context/Auth';
import { useToast } from '@chakra-ui/react';
const UPDATE_CASE_URL_BASE = 'http://localhost:5000/cases/';
const UPDATE_CASE_URL_SUFFIX = '?confirm=';

export default function CasesTable(props) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedCase, setSelectedCase] = useState(null);
  const { token } = useAccessToken();
  const toast = useToast();

  const handleOpenModal = (dCase) => {
    setIsOpen(true);
    setSelectedCase(dCase);
  };

  const handleCloseModal = () => {
    setIsOpen(false);
    setSelectedCase(null);
  };

  const handleCaseAction = (decision) => {
    fetch(
      UPDATE_CASE_URL_BASE +
        selectedCase.id +
        UPDATE_CASE_URL_SUFFIX +
        decision,
      {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token.accessToken}`,
          'Content-Type': 'application/json',
        },
      }
    )
      .then((response) => {
        // Handle the response as needed
        if (response.ok) {
          console.log(response);
          props.updateTable();
          handleCloseModal();

          toast({
            title: 'Done',
            description: 'Case was updated.',
            status: 'success',
            duration: 9000,
            isClosable: true,
          });
        } else {
          toast({
            title: 'Error',
            description: 'An error from the server has occured.',
            status: 'error',
            duration: 9000,
            isClosable: true,
          });
          console.error('Error:', response.status, response);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  let isAcceptButtonDisabled = false;
  let isCancelButtonDisabled = false;
  if (selectedCase) {
    const loggedInUserCaseInfo = selectedCase.user_confirmations.find(
      (user) => user.user_id === props.loggedInUser.id
    );
    console.log(loggedInUserCaseInfo.confirmed);

    isAcceptButtonDisabled = !loggedInUserCaseInfo.can_confirm;
    isCancelButtonDisabled = !loggedInUserCaseInfo.can_cancel;
  }

  return (
    <>
      <Modal isOpen={isOpen} onClose={handleCloseModal} size="auto">
        <ModalOverlay />
        <ModalContent maxW="80%">
          <ModalHeader>
            <HStack justifyContent>
              <Box> Case #{selectedCase?.id.substring(0, 5) + '...'}</Box>
              <Tag size={'md'} variant="solid" colorScheme="blue">
                {getCaseMessage(selectedCase?.status)}
              </Tag>
            </HStack>
          </ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <CaseView dCase={selectedCase} />
          </ModalBody>

          <ModalFooter>
            <Button
              isDisabled={isCancelButtonDisabled}
              variant="ghost"
              mr={3}
              onClick={() => handleCaseAction(false)}
            >
              Decline
            </Button>
            <Button
              isDisabled={isAcceptButtonDisabled}
              variant="ghost"
              onClick={() => handleCaseAction(true)}
            >
              Accept
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <TableContainer
        sx={{
          '&::-webkit-scrollbar': {
            width: '10px',
            height: '10px',
            borderRadius: '16px',
            backgroundColor: `rgba(0, 0, 0, 0.05)`,
          },
          '&::-webkit-scrollbar-thumb': {
            backgroundColor: `blue.200`,
          },
        }}
        overflowY="auto"
        maxHeight="60vh"
        border="2px"
        borderColor="blue.400"
      >
        <Table variant="simple">
          <Thead
            position="sticky"
            top={0}
            bgGradient="linear(to-b, blue.400, teal.400)"
          >
            <Tr>
              <Th color="white">Case Id</Th>
              <Th color="white">Status</Th>
              <Th color="white">Date Added</Th>
              <Th color="white">Marriage-Info</Th>
              <Th color="white">Spouses</Th>
            </Tr>
          </Thead>
          <Tbody>
            {props.cases.length !== 0 ? (
              props.cases.map((divorceCase) => {
                const users = getUsers(divorceCase);

                let tagColorScheme = 'blue';

                if (divorceCase.status === 'CANCELLED') {
                  tagColorScheme = 'red';
                }
                if (divorceCase.status === 'COMPLETED') {
                  tagColorScheme = 'green';
                }

                return (
                  <Tr
                    _hover={{ cursor: 'pointer', bg: 'blue.100' }}
                    key={divorceCase.id}
                    onClick={() => handleOpenModal(divorceCase)}
                  >
                    <Td fontSize={'sm'}>
                      No. {divorceCase.id.substring(0, 5) + '...'}
                    </Td>
                    <Td>
                      <Tag
                        size={'sm'}
                        borderRadius={'full'}
                        colorScheme={tagColorScheme}
                      >
                        <TagLabel>
                          {getCaseMessage(divorceCase.status)}
                        </TagLabel>
                      </Tag>
                    </Td>
                    <Td fontSize={'sm'}>{divorceCase.start_date}</Td>
                    <Td fontSize={'sm'}>
                      ID: {divorceCase.marriage.id.substring(0, 5) + '...'}, R.
                      Date: {divorceCase.marriage.start_date}
                    </Td>
                    <Td>
                      <Flex>
                        <Tag size="sm" border="2px" borderRadius="full">
                          <TagLabel>{users.spouse1Name}</TagLabel>
                        </Tag>
                        <Tag
                          ml="10px"
                          size="sm"
                          border="2px"
                          borderRadius="full"
                        >
                          <TagLabel>{users.spouse2Name}</TagLabel>
                        </Tag>
                      </Flex>
                    </Td>
                  </Tr>
                );
              })
            ) : (
              <Tr>
                <Td>No cases found.</Td>
              </Tr>
            )}
          </Tbody>
        </Table>
      </TableContainer>
    </>
  );
}
