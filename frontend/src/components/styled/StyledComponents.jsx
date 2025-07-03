import { styled } from "@mui/material/styles";
import { Paper, Box, TextField } from "@mui/material";

export const ChatContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  height: "100vh",
  padding: theme.spacing(2),
  backgroundColor: theme.palette.background.default,
}));

export const MessageListContainer = styled(Paper)(({ theme }) => ({
  flex: 1,
  overflow: "auto",
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.spacing(1),
  boxShadow: theme.shadows[1],
}));

export const MessageInputContainer = styled(Box)(({ theme }) => ({
  display: "flex",
  gap: theme.spacing(1),
  padding: theme.spacing(2),
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.spacing(1),
  boxShadow: theme.shadows[1],
}));

export const StyledTextField = styled(TextField)(({ theme }) => ({
  flex: 1,
  "& .MuiOutlinedInput-root": {
    borderRadius: theme.spacing(1),
  },
}));

export const MessageBubble = styled(Paper)(({ theme, isUser }) => ({
  padding: theme.spacing(1.5),
  marginBottom: theme.spacing(1),
  maxWidth: "70%",
  wordWrap: "break-word",
  borderRadius: theme.spacing(1),
  alignSelf: isUser ? "flex-end" : "flex-start",
  backgroundColor: isUser
    ? theme.palette.primary.main
    : theme.palette.grey[200],
  color: isUser
    ? theme.palette.primary.contrastText
    : theme.palette.text.primary,
}));
