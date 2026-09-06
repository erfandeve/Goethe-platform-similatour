"use client";

import { useState } from "react";

import type { Dictionary } from "@/i18n/get-dictionary";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Field";

export function NewsletterForm({ dict }: { dict: Dictionary }) {
  const [done, setDone] = useState(false);

  return (
    <form
      className="mt-5 space-y-3"
      onSubmit={(event) => {
        event.preventDefault();
        setDone(true);
      }}
    >
      <Input
        type="email"
        required
        placeholder={dict.footer.newsletter.placeholder}
        aria-label={dict.footer.newsletter.placeholder}
      />
      <Button type="submit" className="w-full" size="md">
        {done ? dict.footer.newsletter.done : dict.footer.newsletter.cta}
      </Button>
    </form>
  );
}
