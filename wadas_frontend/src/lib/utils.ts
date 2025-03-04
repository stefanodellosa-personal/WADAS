import {refreshAccessToken} from "./auth";

export async function tryWithRefreshing<T>(
    requestFn: () => Promise<T>
): Promise<T> {

    try{
        return await requestFn();
    } catch (error) {
        if (error instanceof Error && error.message.includes("Unauthorized")) {
            await refreshAccessToken();
            return await requestFn();
        } else {
            throw new Error("Unknown error");
        }
    }
}