import { useCallback, useState } from "react";

export const useHttp = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(
    async (
      url,
      method = "GET",
      body = null,
      mode = "cors",
      headers = { "Content-Type": "application/json" }
    ) => {
      setLoading(true);

      try {
        // Make a request
        const response = await fetch(url, { method, mode, headers, body });
        // Process errors
        if (!response.ok) {
          const msg = await response.text();
          throw new Error(JSON.parse(msg).details);
        }
        // Process response
        const data = await response.json();
        setLoading(false);
        return data;
      } catch (e) {
        setLoading(false);
        console.log(e.message);
        setError(e.message);
        throw e;
      }
    },
    []
  );

  const clearError = useCallback(() => setError(null), []);

  return { loading, request, error, clearError };
};
