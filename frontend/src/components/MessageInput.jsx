import { Formik, Form } from "formik";
import * as Yup from "yup";
import { Button } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import {
  MessageInputContainer,
  StyledTextField,
} from "./styled/StyledComponents";

const validationSchema = Yup.object().shape({
  message: Yup.string().required("Please enter a message"),
});

const MessageInput = ({ onSendMessage, isLoading }) => {
  return (
    <Formik
      initialValues={{ message: "" }}
      validationSchema={validationSchema}
      onSubmit={(values, { resetForm }) => {
        onSendMessage(values.message);
        resetForm();
      }}
    >
      {({ values, handleChange, handleBlur, isValid }) => (
        <Form>
          <MessageInputContainer>
            <StyledTextField
              name="message"
              placeholder="Type your message..."
              value={values.message}
              onChange={handleChange}
              onBlur={handleBlur}
              disabled={isLoading}
              fullWidth
              variant="outlined"
              size="medium"
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={!isValid || isLoading}
              endIcon={<SendIcon />}
            >
              Send
            </Button>
          </MessageInputContainer>
        </Form>
      )}
    </Formik>
  );
};

export default MessageInput;
