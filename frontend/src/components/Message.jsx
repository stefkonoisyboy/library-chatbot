import { Typography } from "@mui/material";
import { MessageBubble } from "./styled/StyledComponents";

const Message = ({ text, isUser }) => {
  return (
    <MessageBubble isUser={isUser}>
      <Typography variant="body1">{text}</Typography>
    </MessageBubble>
  );
};

export default Message;
