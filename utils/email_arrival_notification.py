from core.config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv
from io import StringIO
from datetime import date



# 示例 JSON 数据
json_data = [
    {"name": "Alice", "email": "alice@example.com", "age": 25},
    {"name": "Bob", "email": "bob@example.com", "age": 30},
    {"name": "Charlie", "email": "charlie@example.com", "age": 35},
]

# 将 JSON 转为 CSV 数据
def json_to_csv(json_data):
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=json_data[0].keys())
    writer.writeheader()
    writer.writerows(json_data)
    output.seek(0)
    return output.getvalue()


# 将 JSON 转为 HTML 表格
def json_to_html_table(json_data):
    html = "<table border='1' style='border-collapse: collapse;'>"
    # 添加表头
    html += "<tr>" + "".join(f"<th>{key}</th>" for key in json_data[0].keys()) + "</tr>"
    # 添加数据行
    for row in json_data:
        html += "<tr>" + "".join(f"<td>{value}</td>" for value in row.values()) + "</tr>"
    html += "</table>"
    return html

# 发送邮件
def send_email_with_csv_attachment(to_email:list, subject:str, json_data):
    from_email = settings.EMAIL_ACCOUNT
    from_password = settings.PASSWORD

    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = ",".join(to_email)
    msg["Subject"] = subject

    # 将 JSON 数据添加到邮件正文（HTML 表格格式）
    html_content = f"""
    <html>
    <body>
        <div>各位好：</div>
        <div style="height:15px"></div>
        <div>以下产品预计今明到货公司，请相关人员及时安排领料验证，并尽快提供良率数据，以便后续量产安排：</div>
        <div style="height:15px"></div>
        {json_to_html_table(json_data)}
        <div style="height: 150px;"></div>
        <div class="sign" style="width:500px;display: flex;flex-direction: column;">
            <div style="font-size:9px;color:#888;">--------------</div>
            <div style="color:#222222;font-family:arial, sans-serif;line-height:normal;border-collapse:separate;">*************************************************************************************************</div>
            <div style="font-family:宋体;color:#333333;font-size:12px;height: 18px;line-height: 18px;">辛晓飞</div>
            <div style="font-family:宋体;height:18px;font-size:12px;height: 18px;line-height: 18px;">生产制造部</div>
            <div style="display:flex;justify-content: space-between;">
                <!-- <div style="width:150px;height:20px;font-family: Arial, Helvetica, sans-serif;font-size: 12px;line-height: 20px;color: #222222;">电话-0512-68241373</div>
                <div style="width:150px;height:20px;font-family: Arial, Helvetica, sans-serif;font-size: 12px;line-height: 20px;color: #222222;">传真-0512-68259974</div>
                <div style="width:150px;height:20px;font-family: Arial, Helvetica, sans-serif;font-size: 12px;line-height: 20px;color: #222222;">手机-</div> -->
                <div style="margin: 2px 0 2px 0;font-family: Arial, Helvetica, sans-serif;font-size: 12px;color: #222222;">电话-0512-68241373</div>
                <div style="margin: 2px 0 2px 0;font-family: Arial, Helvetica, sans-serif;font-size: 12px;color: #222222;">传真-0512-68259974</div>
                <div style="margin: 2px 0 2px 0;font-family: Arial, Helvetica, sans-serif;font-size: 12px;color: #222222;">手机-&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;</div>
            </div>
            <div style="display:flex;flex-direction:column">
                <div style="font-family:宋体;margin: 2px 0 2px 0;font-size:12px;">苏州华芯微电子股份有限公司</div>
                <div style="font-family:宋体;margin: 2px 0 2px 0;font-size:12px;">地址：苏州高新区向阳路198号资产经营工业园5号楼西一、二层（215011）</div>
                <div style="font-family:宋体;margin: 2px 0 2px 0;font-size:12px;">网址：Http://www.china-chip.com</div>  
            </div>
            <div style="color:#222222;font-family:arial, sans-serif;line-height:normal;border-collapse:separate;">*************************************************************************************************</div>
            <div style="font-family:宋体;color:#333333;font-size:12px;height: auto;line-height: 20px;">
                信息安全声明：本邮件包含信息归发件人所在组织所有,发件人所在组织对该邮件拥有所有权利。
                请接收者注意保密,未经发件人书面许可,不得向任何第三方组织和个人透露本邮件所含信息的全部或部分，
                且除正式书面协议外，所有口头、电子数据及书面内容不作为承担自我约束力的要约或文件。</div>
            <div style="height:auto;font-family: Arial, Helvetica, sans-serif;font-size: 12px;line-height: 20px;color: #222222;">
                Information Security Notice： The information contained in this mail is solely property of the sender's organization.This mail communication is confidential. 
                Recipients named above are obligated to maintain secrecy and are not permitted to disclose the contents of this communication to others.
                And, except a formal written agreement,all verbal, electronic data and written content does not bear the self-binding offer or file.
            </div> 
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    # 添加 CSV 附件
    csv_data = json_to_csv(json_data)
    part = MIMEBase("application", "octet-stream")
    part.set_payload(csv_data.encode("utf-8"))
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f'attachment; filename="lists_{date.today()}.csv"',
    )
    msg.attach(part)
    # 发送邮件
    try:
        with smtplib.SMTP_SSL(settings.IMAP_SERVER, settings.SMTP_PORT) as server:
            # server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
            print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送失败：{e}")