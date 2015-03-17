from openerp.osv import osv, fields

class player_reg(osv.osv):
    _name = "player.reg"
    _rec_name = 'name'

    _columns = {
    'name': fields.char('Player Name'),
    'l_name': fields.char('  '),
    'age': fields.integer('Age'),
    'jersey': fields.integer('Jersey No.'),
    'gplayer': fields.boolean('Is Goal Player'),
    'captain': fields.boolean('Is Captain'),
    'goal': fields.integer('Goal'),
    'ycard': fields.integer('Yellow Card'),
    'rcard': fields.integer('Red Card'),
    'info_id': fields.many2many('team.reg', 'm_id', 'parent_id', 'child_id', "Player Id"),
    }

    
class team_reg(osv.osv):
	_name = "team.reg"
	_rec_name = 't_name'
	
	_columns = {
	't_name': fields.char('Team Name'),
	'flag': fields.boolean('Flag'),
	'n_player': fields.integer('No. Of Player'),
	'coach': fields.many2one('res.partner', 'Coach Name'),
	'win': fields.integer('Win'),
	'lose': fields.integer('Lose'),
	'draw': fields.integer('Draw'),
	'p_list': fields.many2many('player.reg', 'many_id', 'parent_id', 'child_id', "Player List"),
	'p_name': fields.many2one('player.reg', 'Player Name'),
	'pl_list': fields.one2many('p.line','a_id','Player Info'),
	}
	
	
	'''def onchange_p_name(self, cr, uid, ids, n_player, context):
	  if n_player:
	  	
	  
		y=self.pool.get('tab.info').browse(cr, uid, n_player, context)
		
		#print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",y.player_id
		print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",n_player
		val={
			#y.player_id:'n_player'
			#y.'player_id':n_player,
			}
		#print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",y.'player_id'
		return{'value': val}'''
    
	
	
class fixture_info(osv.osv):
	_name = "fixture.info"
	_rec_name = 'refree'
	
	_columns = {
	'state': fields.selection([
            ('plan','Plan'),
            ('game','Game On'),
            ('finish','Finished'),
            ], 'state', readonly=True),
	'team_a': fields.many2one('team.reg', 'Team A'),
	'team_b': fields.many2one('team.reg', 'Team B'),
	'refree': fields.many2one('refree.fifa', 'Refree'),
	'date': fields.date('Date'),
	'score_a': fields.integer('Score A'),
	'score_b': fields.integer('Score B'),
	'result': fields.char('Result'),
	'tab_id': fields.one2many('tab.info', 'i_id',"Goals Lines"),
	'ytab_id': fields.one2many('yellow.lines', 'y_id', 'Yellow'),
	'rtab_id': fields.one2many('red.lines', 'r_id', 'Red'),
	'ctab_id': fields.one2many('ckick.lines', 'c_id', 'Corner'),
	'ptab_id': fields.one2many('pkick.lines', 'p_id', 'Penalty'),
	}
	_defaults = {
        'state': 'plan',
    }

    
	def onchange_p(self, cr, uid, ids, player, context): 
		y= self.pool.get('team.reg').browse(cr, uid, player, context) 
		print "77777777777777777777777777", y.t_name
		if y:
			y.create({'flag': True})
			#return {'value': {'flag': True}}
		return True
    
	'''def onchange_team_a(self, cr, uid, ids,a, context): 
		y= self.pool.get('fixture.info').browse(cr, uid,a, context) 
		print "1111111111111111111", y.t_name
		if y:
			tab_info_obj = self.pool.get('team.reg')
			#print ">>>>>>>>>>>>>>>", y.team_a
			tab_info_obj.create(cr, uid, {'y.team_a.flag': True})
			#return {'value': {'flag': True}}
		return True'''
    
	def fix_plan(self, cr, uid, ids):
		return True

	def fix_game(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'game' })
		return True

	def fix_finish(self, cr, uid, ids):
		self.write(cr, uid, ids, { 'state' : 'finish' })
		return True

class refree_fifa(osv.osv):
    _name="refree.fifa"
    _rec_name="r_name"
   
    _columns={
        'r_name': fields.char("Name"),
        'ylw_awrd':fields.integer("Yellow Card Awarded"),
        'red_awrd':fields.integer("Red Card Awarded"),
        'match_ref':fields.integer("Matches Referred"),
        'ratings': fields.selection([('one',"1"),('two',"2"),('three',"3"),('four',"4"),('five',"5")],("Ratings(out of 5)")),
        'type': fields.selection([('soft',"Soft"),('avg',"Average"),('strct',"Strict")],("Type")),
        'fdbk': fields.text("Feedback"),
        }
        
        
class tab_info(osv.osv):
	_name="tab.info"

	_columns={
    't_team': fields.char('Team'),
    't_player': fields.char('Player'),
    't_goal': fields.integer('Goal'),
    't_date': fields.datetime('Date'),
    'player': fields.integer('NO.Of Player'),
    'i_id': fields.many2one('fixture.info', 'Info'),
    }
    
   	
	'''def appro(self, cr, uid, ids, context=None):
		list_ids = self.browse(cr, uid, ids, context)
		print ">>>>>>>>>", list_ids
		for data in list_ids:
        f=self.pool.get('tab.info').browse(cr, uid, context['active_id'])
		if data.goal == True:
			tab_info_obj = self.pool.get('player.reg')
			for item in f:
				data_id = tab_info_obj.create(cr, uid, {'goal': data.t_goal}, context=None)
		return True'''

class yellow_lines(osv.osv):
	_name="yellow.lines"

	_columns={
	'y_team': fields.char('Team'),
	'y_player': fields.char('Player'),
	'y_card': fields.integer('Yellow Card'),
	'y_date': fields.datetime('Date'),
	'y_id': fields.many2one('fixture.info', 'Info'),
	}
	
class red_lines(osv.osv):
	_name="red.lines"

	_columns={
	'r_team': fields.char('Team'),
	'r_player': fields.char('Player'),
	'r_card': fields.integer('Red Card'),
	'r_date': fields.datetime('Date'),
	'r_id': fields.many2one('fixture.info', 'Info'),
	}
	
class ckick_lines(osv.osv):
	_name="ckick.lines"

	_columns={
	'c_team': fields.char('Team'),
	'c_player': fields.char('Player'),
	'c_kick': fields.integer('Corner Kick'),
	'c_date': fields.datetime('Date'),
	'c_id': fields.many2one('fixture.info', 'Info'),
	}
	
class pkick_lines(osv.osv):
	_name="pkick.lines"

	_columns={
	'p_team': fields.char('Team'),
	'p_player': fields.char('Player'),
	'p_kick': fields.integer('Penalty Kick'),
	'p_date': fields.datetime('Date'),
	'p_id': fields.many2one('fixture.info', 'Info'),
	}
		
class p_line(osv.osv):
	'''def pl(self, cr, uid, ids, context=None): 
		y= self.pool.get('team.reg')
		print "00000000000000000000", y
		for data in y.browse(cr, uid, ids, context=context): 
			print "77777777777777777777777777", data
		tab_info_obj = self.pool.get('p.line')
		return {'value': {'pl_name': y.p_name.name}}'''
		
	_name="p.line"

	def default_get(self, cr, uid, fields, context=None):
		""" 
			To fetch values from stock moves into stock.move.split
		"""
		if context is None:
			context = {}
		print ".........", fields
		res = super(p_line, self).default_get(cr, uid, fields, context=context)
		print "0000000000000000", res.context
		if context.get('active_id'):
			move = self.pool.get('player.reg').browse(cr, uid, context['active_id'], context=context)
			print ".......................", move
			if 'p_name' in fields:
				res.update({'pl_name': move.p_name.id})
		'''if 'unit_cases' in fields:
			res.update({'unit_cases': move.unit_cases})
			if 'use_exist' in fields:
			res.update({'use_exist': True})'''
		return res

	_columns={
	'pl_name': fields.char('Player Name'),
	'a_id': fields.many2one('team.reg','abc'),
	}
	
	'''_defaults = {
        'pl_name': pl,
    }'''
    
	
    
