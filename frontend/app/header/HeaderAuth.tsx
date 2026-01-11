"use client";

import { LoginLink, RegisterLink, LogoutLink } from "@kinde-oss/kinde-auth-nextjs";
import { useKindeBrowserClient } from "@kinde-oss/kinde-auth-nextjs";

export default function HeaderAuth() {
    const { isAuthenticated, isLoading, getUser } = useKindeBrowserClient();
    const user = getUser();

    if (isLoading) return null;

    return (
        <div className="px-1 py-1.5 h-full flex">
            {!isAuthenticated && (
                <>
                    <button className="px-8 text-base font-normal hidden md:block">
                        <LoginLink>Login</LoginLink>
                    </button>
                    <button className="px-8 h-full rounded-full bg-cyan-900 text-neutral-50 text-base font-bold flex items-center hover:bg-cyan-800 transition-all ease-linear duration-50 mr-0.75">
                        <RegisterLink>
                            <span>Sign Up</span>
                        </RegisterLink>
                    </button>
                </>
            )}
            {isAuthenticated && (
                <div className="px-4 hidden md:flex items-center text-base font-semibold text-cyan-950">
                    Hi {user?.given_name || user?.email || "User"} !
                </div>
            )}
            {isAuthenticated && (
                <button className="px-8 h-full rounded-full bg-cyan-900 text-neutral-50 text-base font-bold flex items-center hover:bg-cyan-800 transition-all ease-linear duration-50 mr-0.75">
                    <LogoutLink>
                        <span>Logout</span>
                    </LogoutLink>
                </button>
            )}
        </div>
    );
}
