import { configureStore } from "@reduxjs/toolkit";
import { chatApi } from "../services/api";
import chatReducer from "./chatSlice";

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    [chatApi.reducerPath]: chatApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(chatApi.middleware),
});
