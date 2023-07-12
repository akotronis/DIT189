import {
  Box,
  Button,
  Checkbox,
  FormControl,
  FormHelperText,
  FormLabel,
  Input,
  Textarea,
} from '@chakra-ui/react';
import { Form } from 'react-router-dom';
export default function Create() {
  return (
    <Box maxW="480px">
      <Form method="post" action="create">
        <FormControl isRequired mb="40px">
          <FormLabel>Task name:</FormLabel>
          <Input type="text" name="title"></Input>
          <FormHelperText>Enter a descriptive task name</FormHelperText>
        </FormControl>

        <FormControl mb="40px">
          <FormLabel>Task description:</FormLabel>
          <Textarea
            name="description"
            placeholder="Enter a detailed description for the task..."
          />
        </FormControl>
        <FormControl display="flex" alignItems="center" mb="40px">
          <Checkbox name="isPriority" size="lg" />
          <FormLabel mb="0" ml="10px">
            Make this a priority task
          </FormLabel>
        </FormControl>
        <Button type="submit">Submit</Button>
      </Form>
    </Box>
  );
}

export const createAction = async ({ request }) => {
  const data = await request.formData();

  const task = {
    title: data.get('title'),
    description: data.get('description'),
    isPriority: data.get('isPriority') === '',
  };

  console.log(task);

  return redirect('/');
};
