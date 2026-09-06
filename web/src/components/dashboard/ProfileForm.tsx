"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { Field, Input, Select, Textarea, Toggle } from "@/components/ui/Field";
import type { Dictionary } from "@/i18n/get-dictionary";
import { localeMeta, locales, type Locale } from "@/i18n/config";
import { callApi } from "@/lib/client";
import type { User } from "@/lib/types";
import { LEVEL_ORDER } from "@/lib/utils";

export function ProfileForm({
  user,
  locale,
  dict,
}: {
  user: User;
  locale: Locale;
  dict: Dictionary;
}) {
  const router = useRouter();
  const [values, setValues] = useState(user);
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);

  const [passwords, setPasswords] = useState({ current_password: "", new_password: "" });
  const [passwordError, setPasswordError] = useState("");
  const [passwordDone, setPasswordDone] = useState(false);

  function set<K extends keyof User>(key: K, value: User[K]) {
    setValues((current) => ({ ...current, [key]: value }));
    setSaved(false);
  }

  async function save(event: React.FormEvent) {
    event.preventDefault();
    setBusy(true);
    try {
      const updated = await callApi<User>("auth/me", {
        method: "PATCH",
        body: {
          first_name: values.first_name,
          last_name: values.last_name,
          phone: values.phone,
          bio: values.bio,
          birth_date: values.birth_date,
          city: values.city,
          country: values.country,
          native_language: values.native_language,
          preferred_locale: values.preferred_locale,
          current_level: values.current_level,
          target_level: values.target_level,
          prefs: values.prefs,
        },
        locale,
      });
      setValues(updated);
      setSaved(true);
      router.refresh();
    } finally {
      setBusy(false);
    }
  }

  async function changePassword(event: React.FormEvent) {
    event.preventDefault();
    setPasswordError("");
    setPasswordDone(false);
    try {
      await callApi("auth/change-password", { method: "POST", body: passwords, locale });
      setPasswords({ current_password: "", new_password: "" });
      setPasswordDone(true);
    } catch (caught) {
      setPasswordError((caught as Error).message);
    }
  }

  return (
    <div className="space-y-8">
      <form onSubmit={save} className="glass space-y-6 rounded-3xl p-7">
        <h2 className="font-display text-lg font-semibold">{dict.dashboard.profile.personal}</h2>

        <div className="grid gap-4 sm:grid-cols-2">
          <Field label={dict.auth.firstName}>
            <Input value={values.first_name} onChange={(e) => set("first_name", e.target.value)} />
          </Field>
          <Field label={dict.auth.lastName}>
            <Input value={values.last_name} onChange={(e) => set("last_name", e.target.value)} />
          </Field>
          <Field label={dict.auth.email}>
            <Input value={values.email} disabled dir="ltr" />
          </Field>
          <Field label={dict.auth.phone}>
            <Input value={values.phone} onChange={(e) => set("phone", e.target.value)} dir="ltr" />
          </Field>
          <Field label={dict.dashboard.profile.birthDate}>
            <Input
              type="date"
              value={values.birth_date}
              onChange={(e) => set("birth_date", e.target.value)}
              dir="ltr"
            />
          </Field>
          <Field label={dict.dashboard.profile.city}>
            <Input value={values.city} onChange={(e) => set("city", e.target.value)} />
          </Field>
          <Field label={dict.dashboard.profile.country}>
            <Input value={values.country} onChange={(e) => set("country", e.target.value)} />
          </Field>
        </div>

        <Field label={dict.dashboard.profile.bio}>
          <Textarea value={values.bio} onChange={(e) => set("bio", e.target.value)} />
        </Field>

        <h2 className="font-display pt-2 text-lg font-semibold">
          {dict.dashboard.profile.learning}
        </h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label={dict.dashboard.stats.level}>
            <Select
              value={values.current_level}
              onChange={(e) => set("current_level", e.target.value as User["current_level"])}
            >
              {LEVEL_ORDER.map((level) => (
                <option key={level} value={level} className="bg-ink-900">
                  {level}
                </option>
              ))}
            </Select>
          </Field>
          <Field label={dict.dashboard.stats.target}>
            <Select
              value={values.target_level}
              onChange={(e) => set("target_level", e.target.value as User["target_level"])}
            >
              {LEVEL_ORDER.map((level) => (
                <option key={level} value={level} className="bg-ink-900">
                  {level}
                </option>
              ))}
            </Select>
          </Field>
          <Field label={dict.dashboard.profile.interfaceLanguage}>
            <Select
              value={values.preferred_locale}
              onChange={(e) => set("preferred_locale", e.target.value as Locale)}
            >
              {locales.map((code) => (
                <option key={code} value={code} className="bg-ink-900">
                  {localeMeta[code].native}
                </option>
              ))}
            </Select>
          </Field>
          <Field label={dict.dashboard.profile.nativeLanguage}>
            <Input
              value={values.native_language}
              onChange={(e) => set("native_language", e.target.value)}
            />
          </Field>
        </div>

        <h2 className="font-display pt-2 text-lg font-semibold">{dict.dashboard.profile.prefs}</h2>
        <div className="space-y-2.5">
          <Toggle
            label={dict.dashboard.profile.emailNotif}
            checked={values.prefs.email}
            onChange={(next) => set("prefs", { ...values.prefs, email: next })}
          />
          <Toggle
            label={dict.dashboard.profile.smsNotif}
            checked={values.prefs.sms}
            onChange={(next) => set("prefs", { ...values.prefs, sms: next })}
          />
          <Toggle
            label={dict.dashboard.profile.newsNotif}
            checked={values.prefs.product_news}
            onChange={(next) => set("prefs", { ...values.prefs, product_news: next })}
          />
        </div>

        <div className="flex items-center gap-4 pt-2">
          <Button type="submit" disabled={busy}>
            {busy ? dict.common.loading : dict.dashboard.profile.save}
          </Button>
          {saved ? (
            <span className="text-xs text-mint-400">{dict.dashboard.profile.saved}</span>
          ) : null}
        </div>
      </form>

      <form onSubmit={changePassword} className="glass space-y-4 rounded-3xl p-7">
        <h2 className="font-display text-lg font-semibold">{dict.dashboard.profile.security}</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label={dict.dashboard.profile.currentPassword}>
            <Input
              type="password"
              value={passwords.current_password}
              onChange={(e) => setPasswords({ ...passwords, current_password: e.target.value })}
              dir="ltr"
              required
            />
          </Field>
          <Field
            label={dict.dashboard.profile.newPassword}
            hint={dict.auth.passwordHint}
            error={passwordError}
          >
            <Input
              type="password"
              value={passwords.new_password}
              onChange={(e) => setPasswords({ ...passwords, new_password: e.target.value })}
              dir="ltr"
              required
            />
          </Field>
        </div>
        <div className="flex items-center gap-4">
          <Button type="submit" variant="soft">
            {dict.dashboard.profile.changePassword}
          </Button>
          {passwordDone ? (
            <span className="text-xs text-mint-400">{dict.dashboard.profile.saved}</span>
          ) : null}
        </div>
      </form>
    </div>
  );
}
