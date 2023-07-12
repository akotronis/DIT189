export function getCaseMessage(messageId) {
  switch (messageId) {
    case "WAIT_LAWYER_2":
      return "Pending second lawyer's approval";
    case "WAIT_SPOUSE_1":
      return "Pending spouses' approval";
    case "WAIT_SPOUSE_2":
        return "Pending spouses' approval";
    case "WAIT_10DAYS":
      return 'In the 10-day waiting period';
    case "WAIT_NOTARY":
      return "Pending notary's confirmation";
    case "COMPLETED":
      return 'Case is completed'; 
    case "CANCELLED":
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
