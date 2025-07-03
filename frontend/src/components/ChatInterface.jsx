import { Typography } from "@mui/material";
import { useSelector, useDispatch } from "react-redux";
import { useSendMessageMutation } from "../services/api";
import { addMessage } from "../store/chatSlice";
import MessageList from "./MessageList";
import MessageInput from "./MessageInput";
import { ChatContainer } from "./styled/StyledComponents";

const ChatInterface = () => {
  const messages = useSelector((state) => state.chat.messages);
  const dispatch = useDispatch();
  const [sendMessage, { isLoading }] = useSendMessageMutation();

  const handleSendMessage = async (message) => {
    try {
      dispatch(addMessage({ text: message, isUser: true }));

      const response = await sendMessage(message).unwrap();
      dispatch(addMessage({ text: response.llm_response, isUser: false }));
    } catch (error) {
      console.error("Failed to send message:", error);

      dispatch(
        addMessage({
          text: "Sorry, there was an error processing your message. Please try again.",
          isUser: false,
        })
      );
    }
  };

  return (
    <ChatContainer>
      <Typography variant="h1" gutterBottom align="center">
        Library Chatbot
      </Typography>
      <MessageList messages={messages} />
      <MessageInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </ChatContainer>
  );
};

export default ChatInterface;
