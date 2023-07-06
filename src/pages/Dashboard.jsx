import { HStack, Flex, Heading, Button } from '@chakra-ui/react';
import { PlusSquareIcon } from '@chakra-ui/icons';
import CasesTable from '../components/CasesTable';
import { useDisclosure } from '@chakra-ui/react';
import CustomModal from '../components/CustomModal';
import NewCaseForm from '../components/NewCaseForm';
import { useState, useEffect } from 'react';
export default function Dashboard() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [cases, setCases] = useState([]);

  const handleNewCase = () => {
    onClose();
    fetchData();
  };

  const fetchData = async () => {
    try {
      const response = await fetch(
        'http://localhost:3000/cases'
      ); // Replace with your actual API endpoint
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

  return (
    <>
      <CustomModal isOpen={isOpen} onClose={onClose}>
        <NewCaseForm onClose={handleNewCase} />
      </CustomModal>
      <Flex direction={'column'} gap={'5'}>
        <HStack>
          <Heading as={'h5'} size={'md'}>
            My cases
          </Heading>
          <Button
            onClick={onOpen}
            variant="solid"
            bg="blue.400"
            color="white"
            leftIcon={<PlusSquareIcon />}
          >
            New case
          </Button>
        </HStack>
        <CasesTable cases={cases}/>
      </Flex>
    </>
  );
}
