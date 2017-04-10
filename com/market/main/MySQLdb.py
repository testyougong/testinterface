import paramiko
import ConfigParser

class MySQLdb:
    def MySQL_59(self,sql):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        cf = ConfigParser.ConfigParser()
        cf.read("/Users/zhouxin/PycharmProjects/testinterface/db_config.ini")
        db_host = cf.get("dbconf_59", "db_host")
        db_port = cf.get("dbconf_59", "db_port")
        db_user = cf.get("dbconf_59","db_user")
        db_name = cf.get("dbconf_59","db_name")
        db_path = cf.get("dbconf_59","db_path")

        #sql = "'select sku_id from item_sale limit 10'"

        host = cf.get("sshconf_59","host")
        name = cf.get("sshconf_59","name")
        password = cf.get("sshconf_59","password")
        #print host,name,password

        #print (db_path+" -u"+db_user+" -P"+db_port+" -h"+db_host+" "+db_name+" -N -e "+sql)
        ssh.connect(host,22,name,password)
        stdin, stdout, stderr = ssh.exec_command(db_path+" -u"+db_user+" -P"+db_port+" -h"+db_host+" "+db_name+" -N -e "+sql)
        results = stdout.readlines()
        ssh.close()

        for i in range(1,10):
            print results[i]
            return results[i]

        #ssh.close()
        #return results[i]

    def MySQL_OMS(self, sql):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        cf = ConfigParser.ConfigParser()
        cf.read("/Users/zhouxin/PycharmProjects/testinterface/db_config.ini")
        db_host = cf.get("dbconf_oms", "db_host")
        db_port = cf.get("dbconf_oms", "db_port")
        db_user = cf.get("dbconf_oms", "db_user")
        db_password = cf.get("dbconf_oms", "db_password")
        db_name = cf.get("dbconf_oms", "db_name")
        db_path = cf.get("dbconf_oms", "db_path")

        # sql = "'select sku_id from item_sale limit 10'"

        host = cf.get("sshconf_48", "host")
        name = cf.get("sshconf_48", "name")
        password = cf.get("sshconf_48", "password")
        # print host,name,password

        # print (db_path+" -u"+db_user+" -P"+db_port+" -h"+db_host+" "+db_name+" -N -e "+sql)
        ssh.connect(host, 22, name, password)
        stdin, stdout, stderr = ssh.exec_command(
            db_path + " -u" + db_user + " -p" +db_password +" -P" + db_port + " -h" + db_host + " " + db_name + " -N -e " + sql)
        results = stdout.readlines()
        ssh.close()
        return results[0]
