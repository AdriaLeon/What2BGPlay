import type { User } from "../../types/api";
import "./UserInfo.css";

interface UserInfoProps {
  user: User;
}

export function UserInfo({ user }: UserInfoProps) {
  return (
    <section className="user-info">
      <h2>Profile</h2>

      <div className="user-info-details">
        <div>
          <span className="user-info-label">Username</span>
          <span>{user.username}</span>
        </div>

        <div>
          <span className="user-info-label">Email</span>
          <span>{user.email}</span>
        </div>
      </div>
    </section>
  );
}