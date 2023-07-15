import { HStack, Flex, Heading, Button } from '@chakra-ui/react';
import { PlusSquareIcon } from '@chakra-ui/icons';
import CasesTable from '../components/CasesTable';
import { useDisclosure } from '@chakra-ui/react';
import CustomModal from '../components/CustomModal';
import NewCaseForm from '../components/NewCaseForm';
import { useState, useEffect } from 'react';
import { useAccessToken } from '../context/Auth';
import { decodeAccessToken } from '../utils/keycloak_utils';
import { CASES_FETCH_URL } from '../config/config';

export default function Dashboard(props) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [cases, setCases] = useState([]);
  const { token } = useAccessToken();

  console.log(decodeAccessToken(token.accessToken));

  const handleNewCase = () => {
    onClose();
    fetchData();
  };

  const fetchData = async () => {
    try {
      const response = await fetch(CASES_FETCH_URL, {
        headers: {
          Authorization: `Bearer ${token.accessToken}`,
        },
      }); // Replace with your actual API endpoint
      const data = await response.json();
      console.log(data);
      setCases(data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  // Fetch data when the component mounts
  useEffect(() => {
    fetchData();
  }, []);

  let newCaseButton = null;
  if (props.user.role === 'LAWYER') {
    newCaseButton = (
      <Button
        onClick={onOpen}
        variant="solid"
        bg="blue.400"
        color="white"
        leftIcon={<PlusSquareIcon />}
      >
        New case
      </Button>
    );
  }

  return (
    <>
      <CustomModal isOpen={isOpen} onClose={onClose}>
        <NewCaseForm onClose={handleNewCase} updateTable={fetchData}/>
      </CustomModal>
      <Flex direction={'column'} gap={'5'}>
        <HStack justify={'space-between'}>
          <Heading as={'h5'} size={'md'}>
            My cases
          </Heading>
          {newCaseButton}
        </HStack>
        <CasesTable cases={cases} updateTable={fetchData} loggedInUser={props.user}/>
      </Flex>
    </>
  );
}
