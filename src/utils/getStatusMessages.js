export function getCaseMessage(messageId) {
  switch (messageId) {
    case 1:
      return "Pending second lawyer's approval";
    case 2:
      return "Pending spouses' approval";
    case 3:
      return 'In the 10-day waiting period';
    case 4:
      return "Pending notary's confirmation";
    case 5:
      return 'Case is completed';
    case 6:
      return 'Case is canceled';
    default:
      break;
  }
}
export function getCaseReportHistory(messageId, dCase) {
  let messageArray = [];

  if (messageId === 6) {
    messageArray.push(`The case #${dCase.id} has been canceled. Reason: ${dCase.reason}`);
    return messageArray;
  }
  if (messageId >= 1) {
    messageArray.push(`The case was initialized by lawyer ${dCase.lawyer1Name}.`);
  }
  if (messageId >= 2) {
    messageArray.push(
      `Second lawyer ${dCase.lawyer2Name} has approved the case.`
    );
  }
  if (messageId >= 3) {
    messageArray.push(
      `Spouses ${dCase.spouse1Name} and ${dCase.spouse2Name} have approved the case.`
    );
  }
  if (messageId >= 4) {
    messageArray.push(`The required waiting time of 10 days has passed.`);
  }
  if (messageId >= 5) {
    messageArray.push(
      `Notary ${dCase.notaryName} has approved the case. The divorce is official.`
    );
  }

  return messageArray;
}
