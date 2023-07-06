import {
  Text,
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
} from '@chakra-ui/react';
import { useState } from 'react';
import CaseView from './CaseView';
import { getCaseMessage } from '../utils/getStatusMessages';
export default function CasesTable(props) {
  const [isOpen, setIsOpen] = useState(false);

  const [selectedCase, setSelectedCase] = useState(null);

  const handleOpenModal = (dCase) => {
    setIsOpen(true);
    setSelectedCase(dCase);
  };

  const handleCloseModal = () => {
    setIsOpen(false);
    setSelectedCase(null);
  };

  return (
    <>
      <Modal isOpen={isOpen} onClose={handleCloseModal} size="auto">
        <ModalOverlay />
        <ModalContent maxW="80%">
          <ModalHeader>
            <HStack justifyContent>
              <Box> Case #{selectedCase?.id}</Box>
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
            <Button variant="ghost" mr={3} onClick={handleCloseModal}>
              Decline
            </Button>
            <Button variant="ghost">Accept</Button>
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
          <Thead position="sticky" top={0} bgColor="blue.400">
            <Tr>
              <Th color="white">Case Id</Th>
              <Th color="white">Status</Th>
              <Th color="white">Date Added</Th>
              <Th color="white">Marriage-Info</Th>
              <Th color="white">Spouses</Th>
            </Tr>
          </Thead>
          <Tbody>
            {props.cases &&
              props.cases.map((divorceCase) => (
                <Tr
                  _hover={{ cursor: 'pointer', bg: 'blue.100' }}
                  key={divorceCase.id}
                  onClick={() => handleOpenModal(divorceCase)}
                >
                  <Td fontSize={'sm'}>No. {divorceCase.id}</Td>
                  <Td>
                    <Tag size="sm" colorScheme="blue" borderRadius="full">
                      <TagLabel> {getCaseMessage(divorceCase.status)}</TagLabel>
                    </Tag>
                  </Td>
                  <Td fontSize={'sm'}>{divorceCase.dateAdded}</Td>
                  <Td fontSize={'sm'}>
                    ID: {divorceCase.marriageId}, R. Date:{' '}
                    {divorceCase.registrationDate}
                  </Td>
                  <Td>
                    <Tag size="sm" border="2px" borderRadius="full">
                      <TagLabel>{divorceCase.spouse1Name}</TagLabel>
                    </Tag>
                    <Tag ml="10px" size="sm" border="2px" borderRadius="full">
                      <TagLabel>{divorceCase.spouse2Name}</TagLabel>
                    </Tag>
                  </Td>
                </Tr>
              ))}
          </Tbody>
        </Table>
      </TableContainer>
    </>
  );
}
