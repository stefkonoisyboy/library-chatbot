import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";

export const chatApi = createApi({
  reducerPath: "chatApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:8000" }),
  endpoints: (builder) => ({
    sendMessage: builder.mutation({
      query: (message) => ({
        url: "/query",
        method: "POST",
        body: { text: message },
      }),
    }),
  }),
});

export const { useSendMessageMutation } = chatApi;
