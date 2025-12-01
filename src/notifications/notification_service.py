"""
Firebase Cloud Messaging (FCM) Notification Service
Sends push notifications to mobile devices
"""

import os
import firebase_admin
from firebase_admin import credentials, messaging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class NotificationService:
    """Service for sending push notifications via Firebase Cloud Messaging."""

    def __init__(self):
        """Initialize Firebase Admin SDK."""
        self.initialized = False
        self._initialize_firebase()

    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK with service account."""
        try:
            # Path to Firebase service account JSON
            cred_path = os.getenv(
                "FIREBASE_CREDENTIALS_PATH",
                "config/firebase-serviceaccount.json"
            )

            if not os.path.exists(cred_path):
                print(f"⚠️  Firebase credentials not found at {cred_path}")
                print("⚠️  Notification service running in DEMO mode")
                self.initialized = False
                return

            # Initialize Firebase app
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            self.initialized = True
            print("✅ Firebase Admin SDK initialized successfully")

        except Exception as e:
            print(f"⚠️  Failed to initialize Firebase: {str(e)}")
            print("⚠️  Notification service running in DEMO mode")
            self.initialized = False

    def send_warning_notification(
        self,
        device_token: str,
        warning_message: str,
        location: str,
        severity: str = "medium"
    ) -> bool:
        """
        Send a predictive warning notification to a driver.

        Args:
            device_token: FCM device token
            warning_message: The warning message
            location: Location where warning was triggered
            severity: Warning severity (low, medium, high)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.initialized:
            print(f"📱 [DEMO MODE] Warning notification: {warning_message}")
            return True

        try:
            # Determine notification priority and sound
            priority = "high" if severity == "high" else "normal"
            sound = "warning_high.mp3" if severity == "high" else "warning.mp3"

            # Create notification message
            message = messaging.Message(
                notification=messaging.Notification(
                    title="🚨 Parking Warning",
                    body=warning_message,
                ),
                data={
                    "type": "predictive_warning",
                    "location": location,
                    "severity": severity,
                    "timestamp": datetime.utcnow().isoformat()
                },
                android=messaging.AndroidConfig(
                    priority=priority,
                    notification=messaging.AndroidNotification(
                        sound=sound,
                        color="#FF5722",
                        channel_id="warnings"
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound=sound,
                            badge=1
                        )
                    )
                ),
                token=device_token
            )

            # Send message
            response = messaging.send(message)
            print(f"✅ Warning notification sent: {response}")
            return True

        except Exception as e:
            print(f"❌ Failed to send warning notification: {str(e)}")
            return False

    def send_violation_notification(
        self,
        device_token: str,
        violation_type: str,
        fine_amount: float,
        location: str,
        violation_id: str
    ) -> bool:
        """
        Send a violation notification to a driver.

        Args:
            device_token: FCM device token
            violation_type: Type of violation
            fine_amount: Fine amount
            location: Location of violation
            violation_id: Violation ID

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.initialized:
            print(f"📱 [DEMO MODE] Violation notification: {violation_type} - LKR {fine_amount}")
            return True

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="⚠️ Traffic Violation Detected",
                    body=f"{violation_type} at {location}. Fine: LKR {fine_amount}",
                ),
                data={
                    "type": "violation",
                    "violation_id": violation_id,
                    "violation_type": violation_type,
                    "fine_amount": str(fine_amount),
                    "location": location,
                    "timestamp": datetime.utcnow().isoformat()
                },
                android=messaging.AndroidConfig(
                    priority="high",
                    notification=messaging.AndroidNotification(
                        sound="violation.mp3",
                        color="#D32F2F",
                        channel_id="violations"
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound="violation.mp3",
                            badge=1
                        )
                    )
                ),
                token=device_token
            )

            response = messaging.send(message)
            print(f"✅ Violation notification sent: {response}")
            return True

        except Exception as e:
            print(f"❌ Failed to send violation notification: {str(e)}")
            return False

    def send_payment_confirmation(
        self,
        device_token: str,
        amount: float,
        transaction_id: str
    ) -> bool:
        """
        Send payment confirmation notification.

        Args:
            device_token: FCM device token
            amount: Payment amount
            transaction_id: Transaction ID

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.initialized:
            print(f"📱 [DEMO MODE] Payment confirmation: LKR {amount}")
            return True

        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="✅ Payment Successful",
                    body=f"Your payment of LKR {amount} has been processed successfully.",
                ),
                data={
                    "type": "payment_confirmation",
                    "amount": str(amount),
                    "transaction_id": transaction_id,
                    "timestamp": datetime.utcnow().isoformat()
                },
                android=messaging.AndroidConfig(
                    notification=messaging.AndroidNotification(
                        sound="success.mp3",
                        color="#4CAF50",
                        channel_id="payments"
                    )
                ),
                token=device_token
            )

            response = messaging.send(message)
            print(f"✅ Payment confirmation sent: {response}")
            return True

        except Exception as e:
            print(f"❌ Failed to send payment confirmation: {str(e)}")
            return False

    def send_score_update(
        self,
        device_token: str,
        new_score: int,
        score_badge: str,
        change: int
    ) -> bool:
        """
        Send safety score update notification.

        Args:
            device_token: FCM device token
            new_score: New safety score
            score_badge: Score badge (Excellent, Good, etc.)
            change: Score change (+/-)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not self.initialized:
            print(f"📱 [DEMO MODE] Score update: {new_score} ({score_badge})")
            return True

        try:
            emoji = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            change_text = f"+{change}" if change > 0 else str(change)

            message = messaging.Message(
                notification=messaging.Notification(
                    title=f"{emoji} Safety Score Updated",
                    body=f"Your score is now {new_score}/100 ({score_badge}). Change: {change_text}",
                ),
                data={
                    "type": "score_update",
                    "new_score": str(new_score),
                    "score_badge": score_badge,
                    "change": str(change),
                    "timestamp": datetime.utcnow().isoformat()
                },
                android=messaging.AndroidConfig(
                    notification=messaging.AndroidNotification(
                        sound="default",
                        color="#2196F3",
                        channel_id="updates"
                    )
                ),
                token=device_token
            )

            response = messaging.send(message)
            print(f"✅ Score update notification sent: {response}")
            return True

        except Exception as e:
            print(f"❌ Failed to send score update: {str(e)}")
            return False

    def send_batch_notifications(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict] = None
    ) -> Dict[str, int]:
        """
        Send batch notifications to multiple devices.

        Args:
            device_tokens: List of FCM device tokens
            title: Notification title
            body: Notification body
            data: Optional data payload

        Returns:
            dict: Success and failure counts
        """
        if not self.initialized:
            print(f"📱 [DEMO MODE] Batch notification to {len(device_tokens)} devices")
            return {"success": len(device_tokens), "failure": 0}

        try:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                tokens=device_tokens
            )

            response = messaging.send_multicast(message)
            print(f"✅ Batch sent. Success: {response.success_count}, Failure: {response.failure_count}")

            return {
                "success": response.success_count,
                "failure": response.failure_count
            }

        except Exception as e:
            print(f"❌ Failed to send batch notifications: {str(e)}")
            return {"success": 0, "failure": len(device_tokens)}


# Global notification service instance
notification_service = NotificationService()
