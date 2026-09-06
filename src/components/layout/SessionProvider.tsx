"use client";

import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from "react";

import { callApi } from "@/lib/client";
import type { CartState, User } from "@/lib/types";

interface SessionValue {
  user: User | null;
  cartCount: number;
  unread: number;
  refreshCart: () => Promise<void>;
  setUser: (user: User | null) => void;
}

const SessionContext = createContext<SessionValue>({
  user: null,
  cartCount: 0,
  unread: 0,
  refreshCart: async () => {},
  setUser: () => {},
});

export function SessionProvider({
  children,
  initialUser,
  initialCartCount,
  initialUnread,
}: {
  children: ReactNode;
  initialUser: User | null;
  initialCartCount: number;
  initialUnread: number;
}) {
  const [user, setUser] = useState<User | null>(initialUser);
  const [cartCount, setCartCount] = useState(initialCartCount);

  // Signing in re-renders the server layout with a new session, but useState
  // keeps its first value — so adopt the server's answer whenever it changes.
  // Without this the header still offers "sign in" to someone already signed in.
  const seed = `${initialUser?.id ?? "anon"}:${initialCartCount}:${initialUnread}`;
  const [lastSeed, setLastSeed] = useState(seed);
  if (lastSeed !== seed) {
    setLastSeed(seed);
    setUser(initialUser);
    setCartCount(initialCartCount);
  }

  const refreshCart = useCallback(async () => {
    if (!user) return;
    try {
      const cart = await callApi<CartState>("cart");
      setCartCount(cart.count);
    } catch {
      // A stale session just means the badge stays where it was.
    }
  }, [user]);

  const value = useMemo(
    () => ({ user, cartCount, unread: initialUnread, refreshCart, setUser }),
    [user, cartCount, initialUnread, refreshCart],
  );

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>;
}

export function useSession() {
  return useContext(SessionContext);
}
