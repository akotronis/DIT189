import {
  ChatIcon,
  CheckCircleIcon,
  EmailIcon,
  StarIcon,
  WarningIcon,
} from '@chakra-ui/icons';
import {
  Tab,
  TabList,
  TabPanels,
  Tabs,
  List,
  ListItem,
  ListIcon,
  TabPanel,
} from '@chakra-ui/react';
import React from 'react';

export default function Profile() {
  return (
    <Tabs mt="40px" p="20px" colorScheme="blue" variant="enclosed">
      <TabList>
        <Tab _selected={{ color: 'white', bg: 'blue.200' }}>Account Info</Tab>
        <Tab _selected={{ color: 'white', bg: 'blue.200' }}>Task History</Tab>
      </TabList>
      <TabPanels>
        <TabPanel>
          <List spacing={4}>
            <ListItem>
              <ListIcon as={ChatIcon} />
              Main page
            </ListItem>
            <ListItem>
              <ListIcon as={EmailIcon} />
              Profile
            </ListItem>
            <ListItem>
              <ListIcon as={StarIcon} />
              My Cases
            </ListItem>
          </List>
        </TabPanel>
        <TabPanel>
          <List spacing={4}>
            <ListItem>
              <ListIcon as={CheckCircleIcon} color="teal.400" />
              Lorem ipsum dolor sit amet consectetur.
            </ListItem>
            <ListItem>
              <ListIcon as={CheckCircleIcon} color="teal.400" />
              Lorem ipsum dolor sit amet consectetur.
            </ListItem>
            <ListItem>
              <ListIcon as={WarningIcon} color="red.400" />
              Lorem ipsum dolor sit amet consectetur.
            </ListItem>
            <ListItem>
              <ListIcon as={CheckCircleIcon} color="teal.400" />
              Lorem ipsum dolor sit amet consectetur.
            </ListItem>
            <ListItem>
              <ListIcon as={WarningIcon} color="red.400" />
              Lorem ipsum dolor sit amet consectetur.
            </ListItem>
            <ListItem>
              <ListIcon as={CheckCircleIcon} color="teal.400" />
              Lorem ipsum dolor sit amet consectetur.
            </ListItem>
          </List>
        </TabPanel>
      </TabPanels>
    </Tabs>
  );
}
