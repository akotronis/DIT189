import {
  Box,
  Button,
  FormControl,
  FormHelperText,
  FormLabel,
  Input,
  Text,
  Textarea,
  useToast,
} from '@chakra-ui/react';
import Search from './SearchField';
import { useState } from 'react';
import { Form } from 'react-router-dom';
export default function NewCaseForm(props) {
  const [selectedOption, setSelectedOption] = useState(null);
  const toast = useToast()

  const handleOptionChange = (selectedOption) => {
    setSelectedOption(selectedOption);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    props.onClose();
    // Get the form field values
    const taskName = e.target.elements.title.value;
    const agreementText = e.target.elements.description.value;

    // Prepare the form data for the POST request
    const postData = {
      notary: selectedOption?.value, // Assuming the selected option has a "value" property
      agreementText: agreementText,
      taskName: taskName, // Include other form data properties as needed
    };

    // Perform the POST request using the form data
    fetch('https://endmj05zwk6fe.x.pipedream.net', {
      method: 'POST',
      body: JSON.stringify(postData),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => {
        // Handle the response as needed
        if (response.ok) {
          console.log(response);
          toast({
            title: 'Done',
            description: "A new case was submitted.",
            status: 'success',
            duration: 9000,
            isClosable: true,
          })
        } else {
          toast({
            title: 'Error',
            description: "An error from the server has occured.",
            status: 'error',
            duration: 9000,
            isClosable: true,
          })
          console.error('Error:', response.status);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const isSubmitDisabled = !selectedOption;

  return (
    <Box maxW="480px">
      <Form onSubmit={handleSubmit} method="post" action="create">
        <FormControl isRequired mb="40px">
          <FormLabel>Task name:</FormLabel>
          <Input type="text" name="title"></Input>
        </FormControl>

        <FormControl isRequired mb="40px">
          <FormLabel>Final agreement text:</FormLabel>
          <Textarea
            name="description"
            placeholder="Paste the text of the final agreement here..."
          />
        </FormControl>

        <FormControl mb="40px" isRequired>
          <FormLabel>Notary:</FormLabel>
          <Search value={selectedOption} onChange={handleOptionChange} />
          <FormHelperText>Enter the name of the Notary</FormHelperText>
        </FormControl>
        <Button type="submit" isDisabled={isSubmitDisabled}>
          Submit
        </Button>
      </Form>
    </Box>
  );
}
