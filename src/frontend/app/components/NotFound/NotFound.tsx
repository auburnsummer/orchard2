import { Link } from "@remix-run/react";
import "./NotFound.css";

export function NotFound() {
    return (
        <div className="nf">
            <h1 className="nf_title">404 Not Found</h1>
            <p className="nf_text">Click <Link to="/" className="nf_link">here</Link> to go back to home page</p>
        </div>

    )
}