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
import { getCaseMessage, getUsers } from '../../utils/api_utils';
import { useAccessToken } from '../../context/Auth';
import { useToast } from '@chakra-ui/react';
import { CASES_URL, CASE_UPDATE_URL_SUFFIX, NOTIFICATIONS_URL } from '../../config/config';

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
      CASES_URL + '/' + selectedCase.id + CASE_UPDATE_URL_SUFFIX + decision,
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

          let divorce = selectedCase["id"];

          let logged_in_user = {
            "name": props.loggedInUser["first_name"],
            "surname": props.loggedInUser["last_name"],
            "role": props.loggedInUser["role"],
            "email": props.loggedInUser["email"]
          };

          let state = ""
          switch (selectedCase["status"]) {
            case "WAIT_LAWYER_2":
            case "WAIT_SPOUSE_1":
            case "WAIT_SPOUSE_2":
              if (decision) {
                state = "CONFIRMED";
              }
              else {
                state = "CANCELLED";
              }
              break;
            case "WAIT_10DAYS":
              if (decision) {
                state = "WAITING_PERIOD_STARTED";
              }
              else {
                state = "CANCELLED";
              }
              break;
            case "WAIT_NOTARY":
              if (decision) {
                state = "FINALIZED";
              }
              else {
                state = "CANCELLED";
              }
              break;
            case "COMPLETED":
            case "CANCELLED":
              break;
            default:
              break;
          }

          let recipients = []
          let users = selectedCase["users"]
          users.forEach(user => {
            recipients.push(user["email"])
          });

          let notification = {
            "state": state,
            "divorce": divorce,
            "user": logged_in_user,
            "recipients": recipients
          };

          console.log(notification);

          if (state !== "") {
            fetch(NOTIFICATIONS_URL, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(notification)
            }
            )
              .then((notification_response) => {
                if (notification_response.ok) {
                  console.log(notification_response);
                }
                else {
                  console.error('Error:', notification_response.status, notification_response);
                }
              })
              .catch((notification_error) => {
                console.error('Error sending notification:', notification_error);
              });
          };

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


  }

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