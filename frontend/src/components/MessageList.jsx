import { useEffect, useRef } from "react";
import { Box } from "@mui/material";
import Message from "./Message";
import { MessageListContainer } from "./styled/StyledComponents";

const MessageList = ({ messages }) => {
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <MessageListContainer>
      <Box display="flex" flexDirection="column">
        {messages.map((message, index) => (
          <Message key={index} text={message.text} isUser={message.isUser} />
        ))}
        <div ref={messagesEndRef} />
      </Box>
    </MessageListContainer>
  );
};

export default MessageList;
