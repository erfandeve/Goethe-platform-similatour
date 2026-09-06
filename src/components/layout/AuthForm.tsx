"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Field, Input } from "@/components/ui/Field";
import type { Dictionary } from "@/i18n/get-dictionary";
import type { Locale } from "@/i18n/config";
import { login, register } from "@/lib/client";

export function AuthForm({
  mode,
  locale,
  dict,
}: {
  mode: "login" | "register";
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();

  /**
   * Where to land after signing in. Read at submit time from the address bar
   * rather than through useSearchParams: that hook turns this whole form into a
   * deferred Suspense boundary, and a boundary that fails to stream leaves the
   * page with no form at all.
   */
  function destination() {
    if (typeof window === "undefined") return `/${locale}/dashboard`;
    const target = new URLSearchParams(window.location.search).get("next");
    // Only same-site paths, so a crafted link cannot bounce people off-site.
    return target && target.startsWith("/") && !target.startsWith("//")
      ? target
      : `/${locale}/dashboard`;
  }

  const [values, setValues] = useState({
    email: "",
    password: "",
    confirm: "",
    first_name: "",
    last_name: "",
    phone: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  function update(key: keyof typeof values, value: string) {
    setValues((current) => ({ ...current, [key]: value }));
  }

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    setErrors({});
    setMessage("");

    if (mode === "register" && values.password !== values.confirm) {
      setErrors({ confirm: dict.auth.mismatch });
      return;
    }

    setBusy(true);
    try {
      if (mode === "login") {
        await login(values.email, values.password);
      } else {
        await register({
          email: values.email,
          password: values.password,
          first_name: values.first_name,
          last_name: values.last_name,
          phone: values.phone,
          locale,
        });
      }
      router.push(destination());
      router.refresh();
    } catch (caught) {
      const failure = caught as { fields?: Record<string, string>; message?: string };
      setErrors(failure.fields ?? {});
      setMessage(failure.message ?? dict.common.error);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="space-y-4">
      {mode === "register" ? (
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label={dict.auth.firstName}>
            <Input
              value={values.first_name}
              onChange={(event) => update("first_name", event.target.value)}
              autoComplete="given-name"
            />
          </Field>
          <Field label={dict.auth.lastName}>
            <Input
              value={values.last_name}
              onChange={(event) => update("last_name", event.target.value)}
              autoComplete="family-name"
            />
          </Field>
        </div>
      ) : null}

      <Field label={dict.auth.email} error={errors.email}>
        <Input
          type="email"
          required
          value={values.email}
          onChange={(event) => update("email", event.target.value)}
          autoComplete="email"
          dir="ltr"
        />
      </Field>

      {mode === "register" ? (
        <Field label={dict.auth.phone} error={errors.phone}>
          <Input
            value={values.phone}
            onChange={(event) => update("phone", event.target.value)}
            autoComplete="tel"
            dir="ltr"
          />
        </Field>
      ) : null}

      <Field
        label={dict.auth.password}
        error={errors.password}
        hint={mode === "register" ? dict.auth.passwordHint : undefined}
      >
        <Input
          type="password"
          required
          value={values.password}
          onChange={(event) => update("password", event.target.value)}
          autoComplete={mode === "login" ? "current-password" : "new-password"}
          dir="ltr"
        />
      </Field>

      {mode === "register" ? (
        <Field label={dict.auth.confirmPassword} error={errors.confirm}>
          <Input
            type="password"
            required
            value={values.confirm}
            onChange={(event) => update("confirm", event.target.value)}
            autoComplete="new-password"
            dir="ltr"
          />
        </Field>
      ) : null}

      {message ? (
        <p className="rounded-2xl border border-rose-400/25 bg-rose-400/10 px-4 py-3 text-xs text-rose-400">
          {message}
        </p>
      ) : null}

      <Button type="submit" size="lg" className="w-full" disabled={busy}>
        {busy
          ? dict.common.loading
          : mode === "login"
            ? dict.auth.submitLogin
            : dict.auth.submitRegister}
      </Button>

      <p className="pt-2 text-center text-sm text-mist-500">
        {mode === "login" ? dict.auth.noAccount : dict.auth.hasAccount}{" "}
        <Link
          href={`/${locale}/${mode === "login" ? "register" : "login"}`}
          className="font-semibold text-violet-400 underline-offset-4 hover:underline"
        >
          {mode === "login" ? dict.nav.register : dict.nav.login}
        </Link>
      </p>

      {mode === "register" ? (
        <p className="text-center text-[11px] leading-relaxed text-mist-600">{dict.auth.terms}</p>
      ) : null}
    </form>
  );
}
