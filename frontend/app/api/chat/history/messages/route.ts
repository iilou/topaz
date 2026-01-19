import { NextResponse } from "next/server";
import { getKindeServerSession } from "@kinde-oss/kinde-auth-nextjs/server";

import { CreateChatHistoryMessage } from "@/lib/types/chat";

export async function POST(request: Request) {

    const getUser = getKindeServerSession().getUser;
    const user = await getUser();
    const messageData: CreateChatHistoryMessage = await request.json();

    if (!user) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/chat/history/messages`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": user.id,
            },
            body: JSON.stringify(messageData),
        }
    );

    return NextResponse.json(await res.json());
}

