import React from 'react';
import {
  Card,
  CardBody,
  Text,
  Heading,
  Box,
  Stack,
  StackDivider,
  Tag,
  TagLabel,
  HStack,
  ListIcon,
  List,
  ListItem,
  CardFooter,
} from '@chakra-ui/react';
import { CheckCircleIcon, NotAllowedIcon } from '@chakra-ui/icons';
import { getCaseReportHistory, getUsers } from '../utils/api_utils';

export default function CaseView(props) {
  const users = getUsers(props.dCase);

  const displayedData = {
    dateAdded: props.dCase.start_date,
    lawyer1Name: users.lawyer1Name,
    lawyer2Name: users.lawyer2Name,
    notaryName: users.notaryName,
    spouse1Name: users.spouse1Name,
    spouse2Name: users.spouse2Name,
    marriageId: props.dCase.marriage.id,
    marriageDate: props.dCase.marriage.start_date,
    finalAgreementText: props.dCase.aggrement_text,
  };

  const caseHistoryMessages = getCaseReportHistory(props.dCase, users);

  return (
    <Card>
      <CardBody>
        <Stack divider={<StackDivider />} spacing="4">
          <HStack gap={10} align="start">
            <Box textAlign="center">
              <Heading size="xs" textTransform="uppercase">
                First Lawyer
              </Heading>
              <Text pt="2" fontSize="sm">
                {displayedData.lawyer1Name}
              </Text>
            </Box>
            <Box textAlign="center">
              <Heading size="xs" textTransform="uppercase">
                Second Lawyer
              </Heading>
              <Text pt="2" fontSize="sm">
                {displayedData.lawyer2Name}
              </Text>
            </Box>
            <Box textAlign="center">
              <Heading size="xs" textTransform="uppercase">
                Notary
              </Heading>
              <Text pt="2" fontSize="sm">
                {displayedData.notaryName}
              </Text>
            </Box>
          </HStack>
          <Box>
            <Heading size="xs" textTransform="uppercase" mb="5px">
              Spouses
            </Heading>
            <Tag size="md" border="2px" borderRadius="full">
              <TagLabel>{displayedData.spouse1Name}</TagLabel>
            </Tag>
            <Tag ml="10px" size="md" border="2px" borderRadius="full">
              <TagLabel>{displayedData.spouse2Name}</TagLabel>
            </Tag>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Marriage
            </Heading>
            <Text pt="2" fontSize="sm">
              ID: {displayedData.marriageId}, Registration Date:{' '}
              {displayedData.marriageDate}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Final Agreement text
            </Heading>
            <Text pt="2" fontSize="xs">
              {displayedData.finalAgreementText}
            </Text>
          </Box>
          <Box
            bg={props.dCase.status === 'CANCELLED' ? 'red.200' : 'blue.100'}
            padding="10px"
            borderRadius="10px"
          >
            <List spacing={3}>
              {caseHistoryMessages.map((msg) => (
                <ListItem key={msg}>
                  <ListIcon
                    as={
                      props.dCase.status === 'CANCELLED'
                        ? NotAllowedIcon
                        : CheckCircleIcon
                    }
                    color="green.500"
                  />
                  {msg}
                </ListItem>
              ))}
            </List>
          </Box>
        </Stack>
      </CardBody>
      <CardFooter>
        <Box>
          <Text color="gray.500">Added on: {displayedData.dateAdded}</Text>
        </Box>
      </CardFooter>
    </Card>
  );
}
