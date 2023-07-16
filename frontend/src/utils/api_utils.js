export function getUsers(dCase) {
  let lawyer1 = dCase.user_confirmations.find(
    (user) => user.user_role === 'INITIAL_LAWYER'
  );
  let lawyer2 = dCase.user_confirmations.find(
    (user) => user.user_role === 'SECONDARY_LAWYER'
  );
  let notary = dCase.user_confirmations.find(
    (user) => user.user_role === 'NOTARY'
  );
  let spouse1 = dCase.user_confirmations.find(
    (user) => user.user_role === 'SPOUSE'
  );
  let spouse2 = dCase.user_confirmations.find(
    (user) => user.user_role === 'SPOUSE' && user.user_id !== spouse1.user_id
  );

  if (spouse2.confirmed && !spouse1.confirmed) {
    let temp = { ...spouse1 };
    spouse1 = { ...spouse2 };
    spouse2 = temp;
  }

  lawyer1 = dCase.users.find((user) => user.id === lawyer1.user_id);
  lawyer2 = dCase.users.find((user) => user.id === lawyer2.user_id);
  notary = dCase.users.find((user) => user.id === notary.user_id);
  spouse1 = dCase.users.find((user) => user.id === spouse1.user_id);
  spouse2 = dCase.users.find((user) => user.id === spouse2.user_id);

  const lawyer1Name = lawyer1.first_name + ' ' + lawyer1.last_name;
  const lawyer2Name = lawyer2.first_name + ' ' + lawyer2.last_name;
  const spouse1Name = spouse1.first_name + ' ' + spouse1.last_name;
  const spouse2Name = spouse2.first_name + ' ' + spouse2.last_name;
  const notaryName = notary.first_name + ' ' + notary.last_name;

  const users = {
    lawyer1Name,
    lawyer2Name,
    spouse1Name,
    spouse2Name,
    notaryName,
  };

  return users;
}

export function getCaseMessage(messageId) {
  switch (messageId) {
    case 'WAIT_LAWYER_2':
      return "Pending second lawyer's approval";
    case 'WAIT_SPOUSE_1':
      return "Pending spouses' approval";
    case 'WAIT_SPOUSE_2':
      return "Pending spouses' approval";
    case 'WAIT_10DAYS':
      return 'In the 10-day waiting period';
    case 'WAIT_NOTARY':
      return "Pending notary's confirmation";
    case 'COMPLETED':
      return 'Case is completed';
    case 'CANCELLED':
      return 'Case is canceled';
    default:
      break;
  }
}
export function getCaseReportHistory(dCase, users) {
  let messageArray = [];
  const initStage = `The case was initialized by lawyer ${users.lawyer1Name}.`;
  const secondLawerApprovedStage = `Second lawyer ${users.lawyer2Name} has approved the case.`;
  const spouse1ApprovedStage = `Spouse ${users.spouse1Name} has approved the case.`;
  const spouse2ApprovedStage = `Spouse ${users.spouse2Name} has approved the case.`;
  const tenDaysWaitingStage = `Case was approved by both spouses. 10 days waiting period is initialized.`;
  const tenDaysPassedStage = `The required waiting time of 10 days has passed..`;
  const notaryApprovedStage = `Notary ${users.notaryName} has approved the case. The divorce is official.`;

  if (dCase.status === 'CANCELLED') {
    const responsibleUser = dCase.users.find(
      (user) => user.id === dCase.cancelled_by_id
    );

    messageArray.push(
      `The case #${dCase.id} has been canceled by ${
        responsibleUser.first_name + ' ' + responsibleUser.last_name
      } (ID: ${dCase.cancelled_by_id.substring(0, 5)}...).`
    );
    return messageArray;
  }
  if (dCase.status === 'WAIT_LAWYER_2') {
    messageArray.push(initStage);
  }
  if (dCase.status === 'WAIT_SPOUSE_1') {
    messageArray.push(initStage, secondLawerApprovedStage);
  }

  if (dCase.status === 'WAIT_SPOUSE_2') {
    messageArray.push(
      initStage,
      secondLawerApprovedStage,
      spouse1ApprovedStage
    );
  }

  if (dCase.status === 'WAIT_10DAYS') {
    messageArray.push(
      initStage,
      secondLawerApprovedStage,
      spouse1ApprovedStage,
      spouse2ApprovedStage,
      tenDaysWaitingStage
    );
  }
  if (dCase.status === 'WAIT_NOTARY') {
    messageArray.push(
      initStage,
      secondLawerApprovedStage,
      spouse1ApprovedStage,
      spouse2ApprovedStage,
      tenDaysWaitingStage,
      tenDaysPassedStage
    );
  }
  if (dCase.status === 'COMPLETED') {
    messageArray.push(
      initStage,
      secondLawerApprovedStage,
      spouse1ApprovedStage,
      spouse2ApprovedStage,
      tenDaysWaitingStage,
      tenDaysPassedStage,
      notaryApprovedStage
    );
  }

  return messageArray;
}
