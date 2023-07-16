import {
  Box,
  Button,
  FormControl,
  FormHelperText,
  FormLabel,
  Textarea,
  useToast,
} from '@chakra-ui/react';
import Search from './CaseItemSearchField';
import { useState } from 'react';
import { useAccessToken } from '../../../context/Auth';
import { MARRIAGES_URL, NOTARIES_URL, LAWYERS_URL, CASES_URL } from '../../../config/config';

export default function NewCaseForm(props) {
  const { token } = useAccessToken();
  const [selectedMarriage, setSelectedMarriage] = useState(null);
  const [selectedNotary, setSelectedNotary] = useState(null);
  const [selectedLawyer, setSelectedLawyer] = useState(null);

  const toast = useToast();

  const handleMarriage = (selectedOption) => {
    setSelectedMarriage(selectedOption);
  };

  const handleNotary = (selectedOption) => {
    setSelectedNotary(selectedOption);
  };

  const handleLawyer = (selectedOption) => {
    setSelectedLawyer(selectedOption);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    props.onClose();
    // Get the form field values
    const agreementText = e.target.elements.description.value;

    // Prepare the form data for the POST request
    const postData = {
      marriage_id: selectedMarriage?.value,
      other_lawyer_id: selectedLawyer?.value,
      notary_id: selectedNotary?.value,
      aggrement_text: agreementText,
    };

    // Perform the POST request using the form data
    fetch(CASES_URL, {
      method: 'POST',
      body: JSON.stringify(postData),
      headers: {
        Authorization: `Bearer ${token.accessToken}`,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        console.log(postData);
        // Handle the response as needed
        if (response.ok) {
          console.log(response);
          props.updateTable();
          toast({
            title: 'Done',
            description: 'A new case was submitted.',
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

  const isSubmitDisabled =
    !selectedLawyer || !selectedMarriage || !selectedNotary;

  return (
    <Box maxW="480px">
      <form onSubmit={handleSubmit} method="post" action="create">
        {/* <FormControl isRequired mb="40px">
          <FormLabel>Task name:</FormLabel>
          <Input type="text" name="title"></Input>
        </FormControl> */}
        <FormControl mb="40px" isRequired>
          <FormLabel>Marriage:</FormLabel>
          <Search
            accessToken={token.accessToken}
            url={MARRIAGES_URL}
            value={selectedMarriage}
            onChange={handleMarriage}
          />
          <FormHelperText>Select marriage</FormHelperText>
        </FormControl>
        <FormControl mb="40px" isRequired>
          <FormLabel>Second Lawyer:</FormLabel>
          <Search
            accessToken={token.accessToken}
            url={LAWYERS_URL}
            value={selectedLawyer}
            onChange={handleLawyer}
          />
          <FormHelperText>Select second lawyer</FormHelperText>
        </FormControl>
        <FormControl mb="40px" isRequired>
          <FormLabel>Notary:</FormLabel>
          <Search
            accessToken={token.accessToken}
            url={NOTARIES_URL}
            value={selectedNotary}
            onChange={handleNotary}
          />
          <FormHelperText>Select notary</FormHelperText>
        </FormControl>
        <FormControl isRequired mb="40px">
          <FormLabel>Final agreement text:</FormLabel>
          <Textarea
            name="description"
            placeholder="Paste the text of the final agreement here..."
          />
        </FormControl>
        <Button type="submit" isDisabled={isSubmitDisabled}>
          Submit
        </Button>
      </form>
    </Box>
  );
}