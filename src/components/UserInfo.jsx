import {
  Card,
  CardHeader,
  Heading,
  StackDivider,
  Box,
  Stack,
  Text,
  CardBody,
} from '@chakra-ui/react';


export default function UserInfo(props) {
  return (
    <Card bgGradient="linear(to-b, blue.400, teal.400)" color={"white"}>
      <CardHeader>
        <Heading size="md">Info</Heading>
      </CardHeader>

      <CardBody >
        <Stack divider={<StackDivider />} spacing="2">
          <Box>
            <Heading size="xs" textTransform="uppercase" mb={1}>
              Fullname
            </Heading>
            <Text pt="2" fontSize="sm">
              {props.user.first_name + ' ' + props.user.last_name}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase" mb={1}>
              Username
            </Heading>
            <Text pt="2" fontSize="sm">
              {props.user.username}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase" mb={1}>
              Email
            </Heading>
            <Text pt="2" fontSize="sm">
              {props.user.email}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase" mb={1}>
              VAT
            </Heading>
            <Text pt="2" fontSize="sm">
              {props.user.vat_num}
            </Text>
          </Box>

          <Box>
            <Heading size="xs" textTransform="uppercase" mb={1}>
              Role
            </Heading>
            <Text pt="2" fontSize="sm">
              {props.user.role}
            </Text>
          </Box>
        </Stack>
      </CardBody>
    </Card>
  );
}
