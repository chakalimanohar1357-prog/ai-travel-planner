import React, { useEffect, useState } from "react";
import { Star, Trash2 } from "lucide-react";
import api from "../api/axios";
import { useAuth } from "../context/AuthContext";

function StarInput({ value, onChange }) {
    return (
        <div className="flex gap-1">
            {[1, 2, 3, 4, 5].map((n) => (
                <button key={n} type="button" onClick={() => onChange(n)}>
                    <Star
                        size={22}
                        className={n <= value ? "fill-yellow-400 text-yellow-400" : "text-gray-300"}
                    />
                </button>
            ))}
        </div>
    );
}

export default function ReviewSection({ destinationId }) {
    const { user } = useAuth();
    const [reviews, setReviews] = useState([]);
    const [averageRating, setAverageRating] = useState(0);
    const [totalReviews, setTotalReviews] = useState(0);
    const [myRating, setMyRating] = useState(0);
    const [myComment, setMyComment] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    const loadReviews = () => {
        api.get(`/reviews/destinations/${destinationId}`).then((res) => {
            setReviews(res.data.reviews);
            setAverageRating(res.data.average_rating);
            setTotalReviews(res.data.total_reviews);
        });
    };

    useEffect(() => { loadReviews(); }, [destinationId]);

    const submitReview = async (e) => {
        e.preventDefault();
        setError("");
        if (myRating === 0) {
            setError("Please select a star rating.");
            return;
        }
        setSubmitting(true);
        try {
            await api.post(`/reviews/destinations/${destinationId}`, {
                rating: myRating,
                comment: myComment,
            });
            setMyRating(0);
            setMyComment("");
            loadReviews();
        } catch (err) {
            setError(err.response?.data?.error || "Could not submit review");
        } finally {
            setSubmitting(false);
        }
    };

    const deleteReview = async (reviewId) => {
        if (!window.confirm("Delete your review?")) return;
        await api.delete(`/reviews/${reviewId}`);
        loadReviews();
    };

    return (
        <div>
            <div className="flex items-center gap-3 mb-4">
                <h2 className="text-xl font-display font-semibold text-ink-900">Reviews</h2>
                {totalReviews > 0 && (
                    <span className="flex items-center gap-1 text-sm text-ink-700">
                        <Star size={16} className="fill-yellow-400 text-yellow-400" />
                        {averageRating} ({totalReviews} review{totalReviews !== 1 ? "s" : ""})
                    </span>
                )}
            </div>

            {user && (
                <form onSubmit={submitReview} className="card p-4 mb-6 space-y-3">
                    <p className="text-sm font-medium text-ink-700">Leave a review</p>
                    <StarInput value={myRating} onChange={setMyRating} />
                    <textarea
                        className="input-field"
                        placeholder="Share your experience (optional)"
                        value={myComment}
                        onChange={(e) => setMyComment(e.target.value)}
                        rows={2}
                    />
                    {error && <p className="text-sm text-red-600">{error}</p>}
                    <button type="submit" disabled={submitting} className="btn-primary text-sm">
                        {submitting ? "Submitting..." : "Submit Review"}
                    </button>
                </form>
            )}

            <div className="space-y-3">
                {reviews.length === 0 ? (
                    <p className="text-sm text-ink-500">No reviews yet — be the first to share your experience!</p>
                ) : (
                    reviews.map((r) => (
                        <div key={r.id} className="card p-4">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="font-medium text-ink-900 text-sm">{r.user_name}</p>
                                    <div className="flex gap-0.5 mt-1">
                                        {[1, 2, 3, 4, 5].map((n) => (
                                            <Star key={n} size={13} className={n <= r.rating ? "fill-yellow-400 text-yellow-400" : "text-gray-300"} />
                                        ))}
                                    </div>
                                </div>
                                {user && user.id === r.user_id && (
                                    <button onClick={() => deleteReview(r.id)} className="text-ink-500 hover:text-red-500">
                                        <Trash2 size={15} />
                                    </button>
                                )}
                            </div>
                            {r.comment && <p className="text-sm text-ink-700 mt-2">{r.comment}</p>}
                            <p className="text-xs text-ink-500 mt-1">{new Date(r.created_at).toLocaleDateString()}</p>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}