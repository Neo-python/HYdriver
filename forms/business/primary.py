import wtforms
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired, Optional
from models.business import OrderEntrust
from plugins.HYplugins.form import BaseForm, ListPage
from plugins.HYplugins.form.fields import IdSortField, OrderUuidField
from plugins.HYplugins.form.validators_message import ValidatorsMessage as VM


class AcceptOrderListForm(BaseForm, ListPage, IdSortField):
    """厂家委托单列表"""


class AcceptOrderForm(BaseForm, OrderUuidField):
    """驾驶员接单"""

    def __init__(self, user_uuid, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_uuid = user_uuid

    def validate_order_uuid(self, *args):
        """检验单号"""

        self.entrust = OrderEntrust.query.filter_by(order_uuid=self.order_uuid.data, driver_uuid=self.user_uuid).first()
        
        if not self.entrust:
            raise wtforms.ValidationError(message='此订单无法被您接单,如有疑问,请联系管理员.')

        query = OrderEntrust.query.with_for_update(of=OrderEntrust).filter_by(order_uuid=self.order_uuid.data)
        status = query.filter(OrderEntrust.entrust_status != 0).count()
        if status:
            raise wtforms.ValidationError(message='当前订单已被锁定,已无法接单.')
