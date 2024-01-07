import asyncpg 
from core.utils.percent import pcent

class Request:
    def __init__(self, connector: asyncpg.pool.Pool) -> None:
        self.connector =  connector
    
    async def add_data(self, user_id, user_name, tg_tag):
        query = f"INSERT INTO datausers (user_id, user_name, tg_tag) VALUES ({user_id}, '{user_name}', '@{tg_tag}')"\
                f"ON CONFLICT (user_id) DO UPDATE SET user_name = '{user_name}', tg_tag = '@{tg_tag}'"
        await self.connector.execute(query)
        
    async def check_user(self, user_id):
        query = f"SELECT user_id FROM datausers WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        try:
            user_id = data[0]['user_id']
            return True
        except IndexError:
            return False
            
    
    async def check_balance_rub(self, user_id):
        query = f"SELECT balance_rub FROM datausers WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]

        return data[0]['balance_rub']
    
    async def check_balance_gold(self, user_id):
        query = f"SELECT balance_gold FROM datausers WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        return data[0]['balance_gold']
    
    async def get_kurs(self):
        query = f"SELECT kurs FROM settings"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        return data[0]['kurs']
    
    async def add_balance_gold(self, user_id, gold):
        query = f"UPDATE datausers SET balance_gold = balance_gold + {gold} WHERE user_id = {user_id}"
        await self.connector.execute(query)
        
    async def change_balance_rub(self, user_id, rub):
        query = f"UPDATE datausers SET balance_rub = balance_rub + {rub} WHERE user_id = {user_id}"
        await self.connector.execute(query)

    async def gold_freeze(self, user_id, gold):
        query = f"UPDATE datausers SET freeze_gold = {gold} WHERE user_id= {user_id}"
        await self.connector.execute(query)
    
    async def check_gold_freeze(self, user_id):
        query = f"SELECT freeze_gold FROM datausers WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        return data[0]['freeze_gold']
    
    async def check_user_ref(self, user_id):
        query = f"SELECT ref_users FROM datausers WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        return data[0]['ref_users']
    
    async def save_photo(self, user_id, file_id , sum_out, tg_tag):
        query = f"INSERT INTO out_gold (user_id, file_id, sum_out, tg_tag) VALUES ({user_id}, '{file_id}', {sum_out}, '@{tg_tag}')"\
                f"ON CONFLICT (user_id) DO UPDATE SET file_id = '{file_id}', sum_out = {sum_out}, tg_tag = '@{tg_tag}'"
        await self.connector.execute(query)

    async def get_file(self, min_out, max_out):
        query = f"SELECT file_id, sum_out, tg_tag, user_id FROM out_gold WHERE sum_out >= {min_out} AND sum_out <= {max_out} "
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        data_tuple = {}
        data_tuple['file_id'] = data[0]['file_id']
        data_tuple['sum_out'] = data[0]['sum_out']
        data_tuple['tg_tag'] = data[0]['tg_tag']
        data_tuple['user_id'] = data[0]['user_id']
        return data_tuple
    
    async def get_file_user(self, user_id):
        query = f"SELECT file_id, sum_out, tg_tag, user_id FROM out_gold WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        data_tuple = {}
        data_tuple['file_id'] = data[0]['file_id']
        data_tuple['sum_out'] = data[0]['sum_out']
        data_tuple['tg_tag'] = data[0]['tg_tag']
        data_tuple['user_id'] = data[0]['user_id']
        return data_tuple
    
    async def get_user_out(self, user_id):
        query = f"SELECT user_id FROM out_gold WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        if len(rows) > 0:
            return True
        else: 
            return False
        
        
    async def check_admins(self, user_id):
        query = f"SELECT level, user_id FROM admins WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        if rows == 0:
            return False
        else:
            data = [dict(row) for row in rows]
            data_tuple = {}
            data_tuple['level'] = data[0]['level']
            data_tuple['user_id'] = data[0]['user_id']
            return data_tuple
    
    async def delete_out_gold(self, user_id):
        query = f"DELETE FROM out_gold WHERE user_id = {user_id}"
        await self.connector.execute(query)
    
    
    async def save_photo_recruit(self, file_id, sum_rub, bank, user_id, tg_tag):
        query = f"INSERT INTO recruit_balance (user_id, file_id, sum_rub, bank, tg_tag)"\
                f"VALUES ({user_id}, '{file_id}', {sum_rub}, '{bank}', '@{tg_tag}')"\
                f"ON CONFLICT (user_id) DO UPDATE SET file_id = '{file_id}', sum_rub = {sum_rub}, bank = '{bank}', tg_tag = '@{tg_tag}'"
        await self.connector.execute(query)
    
    async def get_recruit_file(self):
        query = f"SELECT file_id, sum_rub, bank, user_id, tg_tag FROM recruit_balance"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        data_tuple = {}
        data_tuple['file_id'] = data[0]['file_id']
        data_tuple['sum_rub'] = data[0]['sum_rub']
        data_tuple['tg_tag'] = data[0]['tg_tag']
        data_tuple['bank'] = data[0]['bank']
        data_tuple['user_id'] = data[0]['user_id']
        return data_tuple
    
    async def get_recruit_file_user(self, user_id):
        query = f"SELECT file_id, sum_rub, bank, user_id, tg_tag FROM recruit_balance WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        data_tuple = {}
        data_tuple['file_id'] = data[0]['file_id']
        data_tuple['sum_rub'] = data[0]['sum_rub']
        data_tuple['tg_tag'] = data[0]['tg_tag']
        data_tuple['bank'] = data[0]['bank']
        data_tuple['user_id'] = data[0]['user_id']
        return data_tuple
    
    async def delete_recruit(self, user_id):
        query = f"DELETE FROM recruit_balance WHERE user_id = {user_id}"
        await self.connector.execute(query)
        
    async def get_user_recruit(self, user_id):
        query = f"SELECT user_id FROM recruit_balance WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        if len(rows) > 0:
            return True
        else: 
            return False
        
    async def get_promocode(self, promo):
        query = f"SELECT amount_gold, use FROM promocode WHERE name = '{promo}'"
        rows = await self.connector.fetch(query)
        if len(rows) > 0:
            data_d = {}
            data = [dict(row) for row in rows]
            data_d['amount_gold'] = data[0]['amount_gold']
            data_d['use'] = data[0]['use']
            return data_d
        else:
            return 0
    
    async def create_promocode(self, promo, gold, activate):
        query = f"INSERT INTO promocode(name, amount_gold, use) VALUES ('{promo}', {gold}, {activate})"\
                f"ON CONFLICT (name) DO UPDATE SET amount_gold = {gold}, use = {activate}"
        await self.connector.execute(query)

    async def dec_activate_promo(self, name):
        query = f"UPDATE promocode SET use = use - 1 WHERE name = '{name}'"
        await self.connector.execute(query)

    async def delete_promocode(self, promo):
        query = f"DELETE FROM promocode WHERE name = '{promo}'"
        await self.connector.execute(query)
        
    async def all_admins(self):
        query = f"SELECT user_id FROM admins"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        return data


    async def add_ref(self, user_id, ref_id):
        query = f"INSERT INTO ref_info(user_id, ref_id) VALUES ({user_id}, {ref_id})"
        await self.connector.execute(query)
        query = f"UPDATE datausers SET ref_users = ref_users + 1 WHERE user_id = {user_id}"
        await self.connector.execute(query)
    
    async def add_sum_ref(self, ref_id, sum_gold):
        select = f"SELECT user_id FROM ref_info WHERE ref_id = {ref_id}"
        rows = await self.connector.fetch(select)
        data = [dict(row) for row in rows]
        try:
            user_id = data[0]['user_id']
            select = f"SELECT ref_level FROM datausers WHERE user_id = {user_id}"
            rows = await self.connector.fetch(select)
            data = [dict(row) for row in rows]
            ref_level = data[0]['ref_level']
            if ref_level == 1:
                ref_percent = 3
                
            elif ref_level == 2:
                ref_percent = 5
                
            if ref_level == 3:
                ref_percent = 7
                
            sum_gold = pcent(sum_gold, ref_percent)
            query = f"UPDATE ref_info SET ref_sum = ref_sum + {sum_gold} WHERE ref_id = {ref_id}"
            await self.connector.execute(query)
        
            query = f"UPDATE datausers SET ref_sum = ref_sum + {sum_gold}, balance_gold = balance_gold + {sum_gold} WHERE user_id = {user_id}"
            await self.connector.execute(query)
        
        except IndexError:
            return 

    async def get_data_ref(self, user_id):
        query = f"SELECT ref_sum, ref_users, ref_level FROM datausers WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        data_tuple = {}
        data_tuple['ref_sum'] = data[0]['ref_sum']
        data_tuple['ref_users'] = data[0]['ref_users']
        data_tuple['ref_level'] = data[0]['ref_level']
        return data_tuple
    
    async def check_ban(self, user_id):
        query = f"SELECT ban_date, unban_date FROM banlist WHERE user_id = {user_id}"
        rows = await self.connector.fetch(query)
        data = [dict(row) for row in rows]
        print('DAta')
        print(data)
        print(data[0]['unban_date'] - data[0]['ban_date'])
        data_d = {}
        data_d['unban_date'] = data[0]['unban_date']
        data_d['ban_date'] = data[0]['ban_date']
        
        return data_d